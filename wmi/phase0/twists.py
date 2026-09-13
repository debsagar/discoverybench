"""Twist selection study: which twists earn a place, decided by measurement.

Criterion 1 — certifiability rate: fraction of sampled worlds per twist that
  certify (priced out AND compressible) at the lab budget.
Criterion 2 — distinctness matrix D[i][j]: held-out error of the theorist
  restricted to class i (driver family, param searched, own machine search)
  on CERTIFIED worlds of twist j. Diagonal ~0 by certification. Off-diagonal
  ~diagonal => the two twists are the same aha (redundant); high => distinct.
  Row "own" is the memorisation control: what an agent that only knows the
  baseline trick would score.

    python3 -u twists.py [n_seeds] [pool_per_twist]   -> twist_study.json
"""
import json
import sys

from spec import TWISTS, sample_spec
from certify import certify
from enumerator import train_pool, held_out
from theorist import machines, best_in_class, fit_tables, held_err, _select_prefix

H = 3
PARAMS = {"own": [0], "count": range(1, 9), "clock": range(2, 9)}


def certify_rate(twist, n):
    certs = [certify(sample_spec(s, H, twist)) for s in range(n)]
    tally = {v: sum(c["verdict"] == v for c in certs)
             for v in ("CERTIFIED", "SWEEPABLE", "INCOMPRESSIBLE", "REJECT")}
    return tally, [c["seed"] for c in certs if c["verdict"] == "CERTIFIED"]


def class_err(twist, chunks, held):
    driver, h0 = TWISTS[twist]
    infer = h0 == "random"
    sel = _select_prefix(chunks)
    best = None
    for p in PARAMS[driver]:
        e, m = best_in_class(list(machines(H)), sel, driver, p, H, infer)
        if best is None or e < best[0]:
            best = (e, p, m)
    _, p, m = best
    table, _ = fit_tables(m, chunks, driver, p, H, infer)
    return held_err(m, table, held, driver, p, infer)


def main(n_seeds=20, pool_n=3):
    out = {"rates": {}, "pool": {}, "D": {}}
    for tw in TWISTS:
        tally, seeds = certify_rate(tw, n_seeds)
        out["rates"][tw], out["pool"][tw] = tally, seeds[:pool_n]
        print(f"{tw:<9} {tally}  certified seeds: {seeds}", flush=True)
    for i in TWISTS:
        out["D"][i] = {}
        for j in TWISTS:
            errs = []
            for seed in out["pool"][j]:
                spec = sample_spec(seed, H, j)
                errs.append(class_err(i, train_pool(spec, seed, 64), held_out(spec, seed)))
            out["D"][i][j] = round(sum(errs) / len(errs), 4) if errs else None
            print(f"D[class={i:<9}][world={j:<9}] = {out['D'][i][j]}", flush=True)
    json.dump(out, open("twist_study.json", "w"), indent=1)
    print("\nrows = theorist class, cols = world twist")
    print(f"{'':<10}" + "".join(f"{j:>10}" for j in TWISTS))
    for i in TWISTS:
        print(f"{i:<10}" + "".join(f"{str(out['D'][i][j]):>10}" for j in TWISTS))
    print("-> twist_study.json")


if __name__ == "__main__":
    main(*(int(a) for a in sys.argv[1:]))
