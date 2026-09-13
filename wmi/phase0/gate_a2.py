"""Gate A follow-ups: what does finding the CLASS cost?

Experiment 1 — wrong-class theorist: family fixed to "ordinary Markov CA"
  (H=1). Must plateau like the k=0 enumerator: the Gate A win came from the
  latent variable, not Bayes.

Experiment 2 — uncertain-class theorist: MDL selection over the class union
  in theorist.classes() (none / own H=2,3,4 / count(tau) / clock(T)).
  Reported per budget: chosen class and held-out error; the class-discovery
  cost is the extra frames (vs Gate A's 4) before err <= 0.01.

Also: log-budget extrapolation of the k=8 enumerator slope from
  gate_a_results.json — the honest "would need ~2^d x budget" number.
"""
import json
import math

import numpy as np

from spec import sample_spec
from enumerator import train_pool, held_out
from theorist import fit_tables, held_err, select

BUDGETS = (4, 8, 16, 32, 64)


def wrong_class(spec, budgets=BUDGETS):
    held = held_out(spec, spec.seed)
    m = np.zeros((1, 2), np.uint8)
    out = []
    for b in budgets:
        table, _ = fit_tables(m, train_pool(spec, spec.seed, b), "own", 0, 1)
        out.append((b, round(held_err(m, table, held, "own", 0), 4)))
    return out


def uncertain_class(spec, budgets=BUDGETS):
    held = held_out(spec, spec.seed)
    out = []
    for b in budgets:
        chunks = train_pool(spec, spec.seed, b)
        name, H, d, p, m = select(chunks)
        table, _ = fit_tables(m, chunks, d, p, H)
        out.append((b, name, round(held_err(m, table, held, d, p), 4)))
    return out


def extrapolate(path="gate_a_results.json", target=0.01):
    rows = []
    for w in json.load(open(path)):
        errs = [(r["budget_frames"], r["enum"]["8"]) for r in w["curve"]]
        (b1, e1), (b2, e2) = errs[-3], errs[-1]      # slope per doubling, tail
        slope = (e1 - e2) / math.log2(b2 / b1)
        need = ("no measurable progress" if slope < 5e-4
                else f"~2^{(errs[-1][1] - target) / slope:.0f} x current budget")
        rows.append((w["seed"], w["H"], errs[-1][1], round(slope, 4), need))
    return rows


def main():
    for spec in (sample_spec(11, n_hidden=2), sample_spec(21, n_hidden=3),
                 sample_spec(12, n_hidden=3)):
        print(f"\n=== H={spec.n_hidden} seed={spec.seed} ===")
        print("wrong-class (H=1) held-out err:",
              " ".join(f"{b}f:{e}" for b, e in wrong_class(spec)))
        print("uncertain-class theorist:")
        for b, name, e in uncertain_class(spec):
            print(f"  {b:>4} frames  chose {name:<14} err={e}")
    print("\nk=8 enumerator, budget to reach err 0.01 (tail slope per doubling):")
    for seed, H, e, s, need in extrapolate():
        print(f"  H={H} seed={seed:>2}: err@1024={e}  slope={s}  -> {need}")


if __name__ == "__main__":
    main()
