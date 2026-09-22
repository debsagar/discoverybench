"""Module 4: the go/no-go experiment, null-calibrated.

Pipeline per H (2 and 3):
  1. NULL: run truly-Markov (H=1) worlds through the identical pipeline.
     Their err(0) spread is pure finite-sample noise (rare patterns get noisy
     majority votes). Threshold = null median + 3 * null std, so a "gap" only
     counts when it clears what noise alone produces.
  2. Sample worlds; filter dead (activity < 2%), frozen (persistence < 1%),
     and degenerate (effective_H < 2 by occupancy, or occupied rule tables
     that barely disagree on occurring patterns).
  3. Memory depth per world: smallest k with err(k) below threshold ("k>8"
     if even 8 steps of own-cell history don't close the gap — the hard ones).

GO: >= 20% of sampled worlds are usable (alive, non-degenerate, err(0) above
the null threshold).
"""

import numpy as np

from spec import sample_spec
from floor import markov_floor, KS

N_WORLDS = 50
N_NULL = 20
GO_FRACTION = 0.20
MIN_DISAGREEMENT = 0.02   # occupied rule tables must differ on >=2% of occurring patterns


def null_threshold(n_null: int = N_NULL) -> float:
    errs = []
    for seed in range(1000, 1000 + n_null):
        r = markov_floor(sample_spec(seed, n_hidden=1), seed=seed)
        if r["activity"] >= 0.02 and r["persistence_err"] >= 0.01:  # only live nulls
            errs.append(r["err"][0])
    errs = np.array(errs)
    thresh = float(np.median(errs) + 3 * errs.std())
    print(f"null (H=1, truly Markov): {len(errs)} live worlds, "
          f"err(0) median={np.median(errs):.4f} max={errs.max():.4f} -> threshold={thresh:.4f}")
    return thresh


def run(n_hidden: int, thresh: float, n_worlds: int = N_WORLDS) -> None:
    print(f"\n=== H={n_hidden} ===")
    ks_hdr = " ".join(f"{'err(' + str(k) + ')':>8}" for k in KS)
    print(f"{'seed':>4}  {'status':<10} {'act':>5} {ks_hdr} {'depth':>6} {'effH':>4} {'disagr':>6}")

    usable = deep = 0
    for seed in range(n_worlds):
        spec = sample_spec(seed, n_hidden=n_hidden)
        r = markov_floor(spec, seed=seed)
        if r["activity"] < 0.02:
            status = "dead"
        elif r["persistence_err"] < 0.01:
            status = "frozen"
        elif r["effective_H"] < 2 or r["rule_disagreement"] < MIN_DISAGREEMENT:
            status = "degenerate"
        elif r["err"][0] < thresh:
            status = "markov"      # alive but noise-level gap: no hidden signal
        else:
            status = "usable"
            usable += 1

        depth = next((k for k in KS if r["err"][k] < thresh), None)
        depth_s = f"k={depth}" if depth is not None else "k>8"
        if status == "usable" and depth is None:
            deep += 1
        errs = " ".join(f"{r['err'][k]:>8.4f}" for k in KS)
        print(f"{seed:>4}  {status:<10} {r['activity']:>5.2f} {errs} {depth_s:>6} "
              f"{r['effective_H']:>4} {r['rule_disagreement']:>6.3f}")

    need = int(GO_FRACTION * n_worlds)
    print(f"\nusable: {usable}/{n_worlds} (need {need})   deep-memory (gap survives k=8): {deep}")
    print(f"VERDICT H={n_hidden}: {'GO' if usable >= need else 'NO-GO'}")


if __name__ == "__main__":
    thresh = null_threshold()
    for n_hidden in (2, 3):
        run(n_hidden, thresh)
