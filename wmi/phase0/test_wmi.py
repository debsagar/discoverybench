"""Every check here pins a CLAIM the benchmark makes, in the order the paper
makes them. If a test fails, the claim is false (or the code lies about it).

    python3 -m pytest test_wmi.py -v
"""
import numpy as np
import pytest

from spec import WorldSpec, TWISTS, sample_spec
from drivers import signal
from sim import neighbor_counts, rollout, random_state
from floor import markov_floor
from enumerator import train_pool, held_out, enumerator_err, persistence_err
from theorist import theorist_err, fit_tables, held_err, best_in_class, machines
from certify import certify, MAX_THEORY_RES
from pilot import Session, make_probes, render, score_predictions, eval_submitted_model, HIST

GRID = 32


def life():
    b = np.zeros((1, 9), bool); b[0, 3] = True
    s = np.zeros((1, 9), bool); s[0, 2:4] = True
    return WorldSpec(b, s, np.zeros((1, 2), np.uint8))


def alive_world(twist, n_hidden=3, seed0=0):
    """First sampled world of this twist that has something to explain."""
    for seed in range(seed0, seed0 + 40):
        spec = sample_spec(seed, n_hidden, twist)
        V, _ = rollout(spec, *random_state(np.random.default_rng(1), spec, GRID), 40)
        if V[20:].mean() > 0.05 and (V[20:-1] != V[21:]).mean() > 0.05:
            return spec
    raise RuntimeError(f"no alive {twist} world in 40 seeds")


# ---------- ground truth ----------

def test_life_reduction_blinker_and_torus_glider():
    v0 = np.zeros((8, 8), np.uint8); v0[3, 2:5] = 1
    V, _ = rollout(life(), v0, np.zeros_like(v0), 2)
    vert = np.zeros_like(v0); vert[2:5, 3] = 1
    assert np.array_equal(V[1], vert) and np.array_equal(V[2], v0)
    g = np.zeros((6, 6), np.uint8)
    g[0, 1] = g[1, 2] = g[2, 0] = g[2, 1] = g[2, 2] = 1
    V, _ = rollout(life(), g, np.zeros_like(g), 48)
    assert all(V[t].sum() == 5 for t in range(49)), "glider broke on the torus"


def test_driver_signals_mean_what_the_doc_says():
    v = np.zeros((4, 4), np.uint8); v[1, 1] = 1
    c = neighbor_counts(v)
    assert signal("own", 0, v, c, 0)[1, 1] == 1 and signal("own", 0, v, c, 0)[0, 0] == 0
    assert signal("count", 1, v, c, 0)[0, 0] == 1 and signal("count", 2, v, c, 0)[0, 0] == 0
    assert signal("clock", 3, v, c, 2).all() and not signal("clock", 3, v, c, 1).any()


def test_clock_hidden_state_is_global_and_holds_between_ticks():
    spec = sample_spec(0, 2, "clock")
    T = spec.param
    _, Hf = rollout(spec, *random_state(np.random.default_rng(0), spec, 8), 3 * T)
    assert all(np.all(Hf[t] == Hf[t, 0, 0]) for t in range(3 * T + 1))
    assert all(Hf[t, 0, 0] == Hf[t + 1, 0, 0] for t in range(3 * T) if (t + 1) % T)


def test_baseline_seed_stream_unchanged():
    """Seeds 21/12 must still name the Phase 0 / pilot worlds (twist axis is additive)."""
    spec = sample_spec(21, 3)
    assert spec.twist == "own" and spec.birth.sum() == 7 and spec.h_next.tolist() == [[1, 1], [2, 0], [0, 2]]


# ---------- the memory-depth floor ----------

def test_markov_world_has_no_gap_and_oracle_h_is_exact():
    r = markov_floor(sample_spec(7, n_hidden=1))
    assert r["err"][0] < 0.005
    r = markov_floor(sample_spec(7, n_hidden=3))
    assert r["err_h"] < 0.005, "with true h featured the process is deterministic"
    assert r["err"][8] <= r["err"][0] + 0.01, "own-history memory closes the gap for the own twist"


# ---------- enumeration vs induction ----------

def test_markov_world_is_swept_by_the_cheapest_null():
    w = sample_spec(7, n_hidden=1)
    assert enumerator_err(train_pool(w, 7, 64), held_out(w, 7), 0) < 0.01


def test_clock_world_is_swept_by_the_t_table():
    """Honest null: a (pattern, t mod T) table needs no latent to solve a clock world."""
    w = alive_world("clock", 2)
    assert enumerator_err(train_pool(w, 1, 64), held_out(w, 1), "t") < 0.01


@pytest.mark.parametrize("twist", list(TWISTS))
def test_theorist_recovers_every_twist_at_the_certification_budget(twist):
    """Compressibility: with the class given, a short description reaches ~0
    from 64 frames. (16 frames is NOT enough for slow clocks: a tick period of
    6 shows only two hidden transitions, and two machines tie — measured.)"""
    w = alive_world(twist)
    err, _ = theorist_err(train_pool(w, 1, 64), held_out(w, 1), w)
    assert err < 0.01, f"{twist}: theorist err {err}"


def test_wrong_class_theorist_does_not_recover_a_count_world():
    """Distinctness (structural half): the baseline class fails the compressibility
    bar that the true class passes. HOW MUCH it fails by is the study's job (twists.py)."""
    w = alive_world("count")
    chunks, held = train_pool(w, 1, 64), held_out(w, 1)
    right, _ = theorist_err(chunks, held, w)
    _, m = best_in_class(list(machines(3)), chunks, "own", 0, 3)
    wrong = held_err(m, fit_tables(m, chunks, "own", 0, 3)[0], held, "own", 0)
    assert right <= MAX_THEORY_RES < wrong, f"own-class theorist {wrong} vs true {right}"


# ---------- certification ----------

def test_markov_world_is_never_certified():
    assert certify(sample_spec(7, n_hidden=1))["verdict"] != "CERTIFIED"


def test_dead_world_is_rejected():
    z = np.zeros((2, 9), bool)
    c = certify(WorldSpec(z, z, np.array([[1, 1], [0, 0]], np.uint8), seed=0))
    assert c["verdict"] == "REJECT" and c["reason"] == "dead"


# ---------- exam ----------

def test_persistence_agent_scores_exactly_the_floor():
    w = sample_spec(21, 3)
    probes = make_probes(w)
    sc = score_predictions([render(p["given"][-1]) for p in probes], probes)
    assert sc["pred_err"] == sc["persistence_err"] and sc["invalid_replies"] == 0


@pytest.mark.parametrize("twist", list(TWISTS))
def test_submitting_the_true_machine_scores_zero(twist):
    w = alive_world(twist)
    m = {"n_hidden": w.n_hidden, "driver": w.driver, "param": w.param, "h0": w.h0,
         "birth": [np.flatnonzero(r).tolist() for r in w.birth],
         "survive": [np.flatnonzero(r).tolist() for r in w.survive],
         "h_next": w.h_next.tolist()}
    r = eval_submitted_model(str(m).replace("'", '"'), w, make_probes(w))
    assert r["parsed"] and r["model_err"] < 0.01, r


def test_session_enforces_budget_and_hides_h():
    s = Session(sample_spec(21, 3), n_experiments=1)
    out = s.observe({"kind": "soup", "p": 0.5, "seed": 1}, 8, list(range(9)))
    assert "frames" in out and "h" not in out and out["experiments_left"] == 0
    assert "error" in s.observe({"kind": "soup"}, 8, [0])


# ---------- active loop feasibility ----------

def test_true_theory_survives_passive_watching_and_every_poke():
    """active.py's kill counts are meaningful only if the truth is never killed."""
    from active import survivors, outcome, POKES, as_spec
    w = alive_world("count")
    chunks, held = train_pool(w, w.seed, 64), held_out(w, w.seed)
    alive = survivors(chunks, held)
    truth = as_spec(w.driver, w.param, w.h_next, np.stack([w.birth, w.survive], 1).astype(np.uint8))
    assert any(np.array_equal(s.h_next, w.h_next) and s.driver == w.driver and s.param == w.param
               for s in alive), "truth not among survivors"
    assert all(np.array_equal(outcome(truth, *v), outcome(w, *v)) for v in POKES.values())
