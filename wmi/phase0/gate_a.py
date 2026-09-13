"""Gate A: is theory affordable where enumeration is priced out?

Both strategies see the SAME budgeted observations (soup rollout frames) and
are scored on the SAME held-out transitions. Currency: held-out per-cell
prediction error; skill = fraction of the persistence headroom closed.

Enumeration (enumerator.py): majority tables over (3x3 pattern, own-history
  <= k) or (pattern, t mod T). Context space 512 * 2^k; with a budget of B
  frames (~1024*B samples) high-k tables starve and the curve plateaus.
Theory (theorist.py): posits the latent, enumerates the small structured
  machine space, reconstructs h, fits tables by counting. Class GIVEN — this
  gate tests AFFORDABILITY of theory, not discovery of the class (gate_a2).

Verdict criterion: at the largest budget, theorist error ~ 0 while the best
enumerator still pays a visible fraction of the headroom at small-to-mid
budgets — and the theorist reaches near-oracle at budgets where every
enumerator is still far from its own asymptote.
"""
import json

from spec import sample_spec
from enumerator import KS, train_pool, held_out, enumerator_err, persistence_err
from theorist import theorist_err

BUDGETS = (4, 8, 16, 32, 64, 128, 256, 512, 1024)   # total observed frames


def run_world(spec, seed):
    held = held_out(spec, seed)
    rows = []
    for b in BUDGETS:
        chunks = train_pool(spec, seed, b)
        rows.append({"budget_frames": b,
                     "enum": {str(k): round(enumerator_err(chunks, held, k), 4) for k in KS},
                     "theorist": round(theorist_err(chunks, held, spec)[0], 4)})
    return {"seed": spec.seed, "H": spec.n_hidden, "twist": spec.twist,
            "persistence_err": round(persistence_err(held), 4), "curve": rows}


def main():
    worlds = [sample_spec(11, n_hidden=2), sample_spec(21, n_hidden=3),
              sample_spec(22, n_hidden=3), sample_spec(12, n_hidden=3)]
    out = []
    for spec in worlds:
        r = run_world(spec, spec.seed)
        out.append(r)
        print(f"\n=== H={r['H']} seed={r['seed']} twist={r['twist']} persistence_err={r['persistence_err']} ===")
        hdr = " ".join(f"{'k=' + str(k):>7}" for k in KS)
        print(f"{'frames':>7} {hdr} {'theorist':>9}")
        for row in r["curve"]:
            es = " ".join(f"{row['enum'][str(k)]:>7.4f}" for k in KS)
            print(f"{row['budget_frames']:>7} {es} {row['theorist']:>9.4f}")
    with open("gate_a_results.json", "w") as f:
        json.dump(out, f, indent=1)
    print("\n-> gate_a_results.json")


if __name__ == "__main__":
    main()
