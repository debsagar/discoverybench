"""Pilot: LLM-in-the-theorist-seat — environment, exam, scoring. No LLM here.

Protocol: the agent explores a certified world through a budgeted observe()
(soup or chosen pattern, frames rendered as text grids, recorded times of its
choosing — whether it requests consecutive per-cell series is itself data),
then takes a two-layer exam:
  prediction : n probes, each = frames 0..8 of a fresh held-out soup, predict
               frame 9 as a text grid. Frames start at t=0 deliberately — the
               hidden state is reconstructible only from the full prefix, so a
               perfect model can score 0 and persistence is the honest floor.
  declaration: a JSON claim — is the visible frame sufficient? how many hidden
               states? what update rule? — scored against ground truth
               (markov claim vs err(0)>0, H vs effective_H from Phase 0 diag).
"""
import json

import numpy as np

from spec import WorldSpec
from sim import rollout, random_state, step
from drivers import h0_field, DRIVERS
from floor import markov_floor
from theorist import h_fields, infer_h0

GRID = 32
HIST = 9          # frames 0..8 given, predict 9
PROBE_SALT = 555_000


def render(frame):
    return "\n".join("".join(".#"[v] for v in row) for row in frame)


def parse_grid(text):
    """Last block of GRID consecutive grid-ish lines in the reply, or None."""
    lines = [l.strip() for l in text.splitlines()]
    rows, best = [], None
    for l in lines:
        cells = [c for c in l if c in ".#01"]
        if len(cells) >= GRID:
            rows.append([1 if c in "#1" else 0 for c in cells[:GRID]])
            if len(rows) >= GRID:
                best = rows[-GRID:]
        else:
            rows = []
    return np.array(best, np.uint8) if best else None


class Session:
    """Budgeted observation interface. Frames always start at t=0."""

    def __init__(self, spec: WorldSpec, n_experiments=6, max_record=9, max_t=32):
        self.spec = spec
        self.left = n_experiments
        self.max_record, self.max_t = max_record, max_t
        self.trace = []

    def observe(self, init, t, record):
        if self.left <= 0:
            return {"error": "experiment budget exhausted"}
        try:
            t = int(t)
            record = sorted({int(x) for x in record})
        except (TypeError, ValueError):
            return {"error": "t must be an int, record a list of ints"}
        if not 1 <= t <= self.max_t:
            return {"error": f"t must be in [1, {self.max_t}]"}
        if len(record) > self.max_record or any(x < 0 or x > t for x in record):
            return {"error": f"record: <= {self.max_record} times within [0, {t}]"}
        if init.get("kind") == "soup":
            p = float(init.get("p", 0.5))
            if not 0.0 < p < 1.0:
                return {"error": "p must be in (0, 1)"}
            rng = np.random.default_rng(int(init.get("seed", 0)) + 12_345)
            v0 = (rng.random((GRID, GRID)) < p).astype(np.uint8)
        elif init.get("kind") == "pattern":
            v0 = np.zeros((GRID, GRID), np.uint8)
            try:
                for r, c in init["cells"]:
                    v0[int(r) % GRID, int(c) % GRID] = 1
            except (TypeError, ValueError, KeyError):
                return {"error": "pattern needs cells: [[r, c], ...]"}
        else:
            return {"error": "init.kind must be 'soup' or 'pattern'"}
        h0 = h0_field(self.spec, np.random.default_rng(self.spec.seed + 99 * len(self.trace)), v0.shape)
        V, _ = rollout(self.spec, v0, h0, t)
        self.left -= 1
        self.trace.append({"init": init, "t": t, "record": record})
        frames = "\n\n".join(f"t={x}\n{render(V[x])}" for x in record)
        return {"frames": frames, "experiments_left": self.left}


def make_probes(spec, n=6):
    rng = np.random.default_rng(spec.seed + PROBE_SALT)
    probes = []
    for _ in range(n):
        V, _ = rollout(spec, *random_state(rng, spec, GRID), HIST)
        probes.append({"given": V[:HIST], "target": V[HIST]})
    return probes


def probe_prompt(probe, i, n):
    frames = "\n\n".join(f"t={t}\n{render(probe['given'][t])}" for t in range(HIST))
    return (f"PREDICTION PROBE {i + 1}/{n}. Here are frames t=0..{HIST - 1} of a fresh "
            f"rollout of the SAME world (t=0 is a random soup):\n\n{frames}\n\n"
            f"Predict frame t={HIST}. Reply with EXACTLY {GRID} lines of {GRID} "
            f"characters, '.' for dead and '#' for alive, and nothing else.")


DECLARATION_PROMPT = """DECLARATION. State what you believe this world is, as one JSON object,
no other text:
{"visible_frame_sufficient": true|false,   // does the current visible frame fully determine the next?
 "n_hidden_states": <int or null>,          // if not: how many per-cell hidden states do you posit?
 "hidden_update_rule": "<one sentence>",    // what drives the hidden state?
 "mechanism": "<one or two sentences on the visible update rule>",
 "confidence": <0..1>}"""


def score_predictions(replies, probes):
    errs, pers, invalid = [], [], 0
    for reply, probe in zip(replies, probes):
        pred = parse_grid(reply)
        if pred is None:
            invalid += 1
            pred = probe["given"][-1]          # fallback: persistence
        errs.append(float((pred != probe["target"]).mean()))
        pers.append(float((probe["given"][-1] != probe["target"]).mean()))
    return {"pred_err": round(float(np.mean(errs)), 4),
            "persistence_err": round(float(np.mean(pers)), 4),
            "invalid_replies": invalid, "n_probes": len(probes)}


MODEL_PROMPT = """FINAL TASK. Submit your best EXECUTABLE model of the dynamics as one JSON
object, no other text. It will be run on held-out rollouts and scored by
prediction error. Schema (n_hidden=1 means "no hidden state"):
{"n_hidden": <int 1..6>,
 "driver": "own" | "count" | "clock",   // what feeds the hidden update: the cell's own state, 1{neighbors>=param}, or a global tick every param steps
 "param": <int>,                         // tau for count, T for clock, 0 for own
 "h0": "zero" | "random",               // do all cells start in hidden state 0, or in unknown random states?
 "birth":   [<per hidden state: list of neighbor counts 0-8 at which a DEAD cell becomes alive>],
 "survive": [<per hidden state: list of counts at which a LIVE cell stays alive>],
 "h_next":  [<per hidden state: [next h if cell dead, next h if cell alive]>]}
Example for plain B3/S23 with no hidden state:
{"n_hidden":1,"driver":"own","param":0,"h0":"zero","birth":[[3]],"survive":[[2,3]],"h_next":[[0,0]]}"""


def eval_submitted_model(text, spec, probes):
    """Run the submitted machine conditionally on true prefixes: advance h on
    the TRUE frames 0..8 (inferring h0 per cell if the model says random),
    then predict frame 9 with one simulator step."""
    try:
        m = json.loads(text[text.index("{"): text.rindex("}") + 1])
        H = int(m["n_hidden"])
        assert 1 <= H <= 6
        birth = np.zeros((H, 9), bool)
        survive = np.zeros((H, 9), bool)
        for hs in range(H):
            birth[hs, [int(c) for c in m["birth"][hs]]] = True
            survive[hs, [int(c) for c in m["survive"][hs]]] = True
        h_next = np.array([[int(x) % H for x in row] for row in m["h_next"]], np.uint8)
        assert h_next.shape == (H, 2)
        sub = WorldSpec(birth, survive, h_next, driver=m.get("driver", "own"),
                        param=int(m.get("param", 0)), h0=m.get("h0", "zero"))
        assert sub.driver in DRIVERS and sub.h0 in ("zero", "random")
    except (ValueError, KeyError, IndexError, TypeError, AssertionError,
            json.JSONDecodeError) as e:
        return {"parsed": False, "error": str(e)[:120]}
    table = np.stack([birth, survive], 1).astype(np.uint8)        # (H, 2, 9)
    errs = []
    for probe in probes:
        given = probe["given"]
        h0 = (infer_h0(h_next, table, given, sub.driver, sub.param)
              if sub.h0 == "random" else None)
        h = h_fields(h_next, given, sub.driver, sub.param, h0)[HIST - 1]
        pred, _ = step(sub, given[HIST - 1], h, HIST - 1)
        errs.append(float((pred != probe["target"]).mean()))
    return {"parsed": True, "model_err": round(float(np.mean(errs)), 4),
            "n_hidden": H, "driver": sub.driver}


def score_declaration(decl_text, spec):
    fl = markov_floor(spec, seed=spec.seed)
    truth = {"markov": False, "effective_H": fl["effective_H"]}
    try:
        start = decl_text.index("{")
        decl = json.loads(decl_text[start: decl_text.rindex("}") + 1])
    except (ValueError, json.JSONDecodeError):
        return {"parsed": False, "truth": truth}
    said_markov = bool(decl.get("visible_frame_sufficient", True))
    return {"parsed": True, "declaration": decl, "truth": truth,
            "posited_latent": not said_markov,
            "h_match": decl.get("n_hidden_states") == fl["effective_H"],
            "confidence": decl.get("confidence")}
