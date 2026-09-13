"""Gate B: per-world certification of the difficulty triple.

A generated world may only enter the benchmark pool carrying:

  headroom     : persistence (obvious-model) error on held-out rollouts —
                 what there is to explain.
  enum_res     : residual error of the STRONGEST cheap null at the offered
                 budget — best over the enumerator family (own-history k,
                 t mod T). This IS the sweep-cost certificate: it measures the
                 effective (occupied) context space against the budget.
  theory_res   : scripted theorist's error at the SAME budget, class given —
                 the compressibility certificate (a short description
                 provably reaches the headroom within budget).
  desc_bits    : length of that short description (tables + machine + twist).
  n_ctx        : distinct depth-8 contexts occurring in the budgeted
                 observations (diagnostic: occupied sweep space).

Verdict CERTIFIED requires both halves of the principle:
  compressible : theory_res <= 0.01
  priced out   : enum_res >= 0.05 and enum_res >= 0.15 * headroom
Alive-but-sweepable worlds are SWEEPABLE (usable only as easy tier);
dead/frozen/degenerate worlds are REJECT (Phase 0 diagnostics).
"""
import json
import math

from spec import sample_spec, TWISTS
from floor import markov_floor
from enumerator import KS, train_pool, held_out, enumerator_err, persistence_err, feats
from theorist import theorist_err

BUDGET_FRAMES = 64      # the lab budget the certificate is issued against
MIN_ENUM_RES = 0.05
MIN_ENUM_FRAC = 0.15
MAX_THEORY_RES = 0.01


def desc_bits(spec):
    H = spec.n_hidden
    bits = 18 * H + (2 * H * math.log2(H) if H > 1 else 0)
    return round(bits + math.log2(len(TWISTS)) + (3 if spec.param else 0), 1)


def _reject(spec, fl):
    if fl["activity"] < 0.02:
        return "dead"
    if fl["persistence_err"] < 0.01:
        return "frozen"
    if fl["effective_H"] < 2 or fl["rule_disagreement"] < 0.02:
        return "degenerate"
    return None


def certify(spec, budget=BUDGET_FRAMES):
    base = {"seed": spec.seed, "H": spec.n_hidden, "twist": spec.twist}
    reason = _reject(spec, markov_floor(spec, seed=spec.seed))
    if reason:
        return {**base, "verdict": "REJECT", "reason": reason}
    chunks = train_pool(spec, spec.seed, budget)
    held = held_out(spec, spec.seed)
    headroom = persistence_err(held)
    enum_res = min(enumerator_err(chunks, held, k) for k in KS)
    theory_res, _ = theorist_err(chunks, held, spec)
    priced_out = enum_res >= MIN_ENUM_RES and enum_res >= MIN_ENUM_FRAC * headroom
    compressible = theory_res <= MAX_THEORY_RES
    verdict = ("CERTIFIED" if priced_out and compressible
               else "SWEEPABLE" if compressible else "INCOMPRESSIBLE")
    return {**base, "verdict": verdict, "budget_frames": budget,
            "headroom": round(headroom, 4), "enum_res": round(enum_res, 4),
            "theory_res": round(theory_res, 4), "desc_bits": desc_bits(spec),
            "n_ctx_k8": len({int(v) for V in chunks for v in feats(V, 8, 0)[0]})}


def main(n_worlds=50):
    results = []
    for H in (2, 3):
        print(f"\n=== H={H}, budget={BUDGET_FRAMES} frames ===")
        for seed in range(n_worlds):
            c = certify(sample_spec(seed, n_hidden=H))
            results.append(c)
            print(f"{seed:>4} {c['verdict']:<14} " + (c.get("reason", "") if "reason" in c else
                  f"headroom={c['headroom']:.4f} enum={c['enum_res']:.4f} theory={c['theory_res']:.4f}"))
        pool = [c for c in results if c["H"] == H]
        tally = {v: sum(c["verdict"] == v for c in pool) for v in ("CERTIFIED", "SWEEPABLE", "INCOMPRESSIBLE", "REJECT")}
        print(f"H={H}: {tally} of {len(pool)}")
    with open("certificates.json", "w") as f:
        json.dump(results, f, indent=1)
    print("\n-> certificates.json")


if __name__ == "__main__":
    main()
