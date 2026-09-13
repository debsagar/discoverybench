"""Feasibility: can the current generator host the active loop?

A world is ACTIVE when, after 64 passive frames, some compact theory other
than the truth still explains everything (train err 0 AND fresh-soup err 0),
yet a simple poke makes it predict something different from the truth.

    python3 active.py own 20      # -> active.json
"""
import json
import sys

import numpy as np

from spec import WorldSpec, sample_spec
from sim import rollout
from enumerator import train_pool, held_out
from theorist import machines, fit_tables, held_err
from floor import markov_floor
from certify import _reject

G, T_POKE = 32, 8
TOL = 1e-4     # ponytail: a context unseen in 64 frames costs the truth a few held-out cells


def as_spec(d, p, m, table):
    """A fitted theory IS a world: table[h, v, count] -> birth/survive rows."""
    return WorldSpec(table[:, 0].astype(bool), table[:, 1].astype(bool), m, driver=d, param=p)


def hypotheses():
    """(driver, param, H): the space the generator draws from (H=2,3)."""
    for H in (2, 3):
        yield "own", 0, H
        for tau in range(1, 9):
            yield "count", tau, H


def survivors(chunks, held):
    """Theories with zero error on the passive budget AND on fresh soups."""
    out = []
    for d, p, H in hypotheses():
        for m in machines(H):
            table, e = fit_tables(m, chunks, d, p, H)
            if e == 0 and held_err(m, table, held, d, p) <= TOL:
                out.append(as_spec(d, p, m, table))
    return out


def _block(v, r, c, n, val=1):
    v = v.copy(); v[r:r + n, c:c + n] = val; return v


def _soup(p, seed=0):
    return (np.random.default_rng(seed).random((G, G)) < p).astype(np.uint8)


POKES = {                                  # name: (v0, mid-run edit or None)
    "block":  (_block(np.zeros((G, G), np.uint8), 12, 12, 8), None),
    "sparse": (_soup(0.1), None),
    "dense":  (_soup(0.85), None),
    "fill":   (_soup(0.5), lambda v: _block(v, 14, 14, 4)),
    "clear":  (_soup(0.5), lambda v: _block(v, 12, 12, 8, 0)),
}


def outcome(spec, v0, edit):
    """Frames after the poke; hidden state carried through a mid-run edit."""
    V, Hf = rollout(spec, v0, np.zeros_like(v0), T_POKE)
    if edit is None:
        return V[1:]
    return rollout(spec, edit(V[-1]), Hf[-1], T_POKE)[0][1:]   # ponytail: t restarts; only clock cares


def audit(spec):
    """Per poke: how many otherwise-indistinguishable theories the poke kills."""
    chunks, held = train_pool(spec, spec.seed, 64), held_out(spec, spec.seed)
    alive = survivors(chunks, held)
    truth = {k: outcome(spec, *v) for k, v in POKES.items()}
    killed = {k: sum(not np.array_equal(outcome(s, *POKES[k]), truth[k]) for s in alive)
              for k in POKES}
    return {"seed": spec.seed, "twist": spec.twist, "alive": len(alive), "killed": killed,
            "active": any(killed.values())}


def main(twist="own", n=20, H=3):
    rows = []
    for seed in range(n):
        spec = sample_spec(seed, H, twist)
        reason = _reject(spec, markov_floor(spec, seed=seed))
        if reason in ("dead", "frozen"):
            continue
        r = {**audit(spec), "degenerate": reason == "degenerate"}
        rows.append(r)
        json.dump(rows, open(f"active_{twist}.json", "w"), indent=1)
        print(r, flush=True)
    print(f"ACTIVE {sum(r['active'] for r in rows)}/{len(rows)} "
          f"(non-degenerate {sum(r['active'] and not r['degenerate'] for r in rows)})")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "own", int(sys.argv[2]) if len(sys.argv) > 2 else 20)
