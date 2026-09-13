# Phase 0 — hidden-variable CA: does the premise hold?

Claim under test (corrected after review): since h0 = 0 and h' = h_next[h][own v],
each cell's hidden state is a deterministic function of its own visible history —
so the world is learnable, and a visible-only predictor must **use history or
posit a latent**. Phase 0 measures how much history: the memory depth of each
world, calibrated against a truly-Markov null.

**Result (2026-09-01): GO at both H=2 and H=3.**
- Null (15 live H=1 worlds through the identical pipeline): err(0) median 0.0000,
  max 0.0005 → threshold = median + 3σ = 0.0004.
- H=2: 26/50 usable (alive, effective_H ≥ 2, table disagreement ≥ 2%, err(0)
  above null); 22 keep a gap at k=8.
- H=3: 34/50 usable; 31 keep a gap at k=8; err(0) up to 0.37, err(8) up to 0.25.
- Control err_h (predictor given true h) ≤ 0.0005 everywhere.
- Caveat: the deterministic simulator makes the null razor-tight, so binary
  "k>8" includes worlds with tiny residual gaps (~0.002). Use the err(8)
  magnitude, not the binary depth, as the hardness axis when curating.

## Modules (claims are pinned in `test_wmi.py`; structure in `MAP.md`)

| file | role | run |
|---|---|---|
| `spec.py` | World = per-hidden-state B/S tables + hidden machine `h_next[h][v]`, seeded sampler. | `python3 spec.py` |
| `sim.py` | Ground-truth simulator; reduces exactly to Conway's Life at H=1 (blinker, wrapping glider). | `python3 sim.py` |
| `floor.py` | err(k) memory-depth curve for k=0,1,2,4,8: majority-vote over (3×3 pattern, own v at t−1..t−k); err_h control (must be ~0); degeneracy diagnostics (h occupancy → effective_H, occurrence-weighted rule disagreement). | `python3 floor.py` |
| `experiment.py` | Null-calibrated go/no-go for H=2 and H=3: filter dead/frozen/degenerate/noise-level worlds, report err(k) curves and memory depth. | `python3 experiment.py` |
| `drivers.py` | The twist axis: `h' = m[h, d]` with driver signal d ∈ {own v, 1{count≥τ}, global tick every T}; h0 zero or hidden-random. One definition shared by simulator and theorist. | — |
| `enumerator.py` | Null family: majority tables over (pattern, own-history k) and (pattern, t mod T); budgeted data pools. | — |
| `theorist.py` | Scripted induction: enumerate machines, reconstruct/infer h, fit tables by counting, MDL class selection over the union. | — |
| `certify.py` | Gate B verdict per world (CERTIFIED / SWEEPABLE / INCOMPRESSIBLE / REJECT). | `python3 certify.py` |
| `twists.py` | Twist selection study: certifiability rate per twist + class-distinctness matrix. | `python3 -u twists.py 20 3` |
| `test_wmi.py` | One test per claim (Life reduction, oracle exactness, sweeps, compressibility per twist, distinctness, certification, exam). | `python3 -m pytest test_wmi.py -q` |

## Twists (one world family, several ahas)

| twist | driver d | h0 | aha | what reveals it |
|---|---|---|---|---|
| `own` | own v | zero | cells remember their own past | same pattern, different pasts, different futures |
| `count` | 1{neighbors ≥ τ} | zero | cells remember their crowd | isolated vs crowded copies of a cell |
| `clock` | tick every T steps | zero | rule changes with time, globally | same soup diverges at fixed times; **swept by a (pattern, t mod T) table**, so rarely certifies |
| `own_h0` | own v | hidden random | must *infer* per-cell state, not reconstruct it | identical placed patterns behave differently at t=0 |
| `count_h0` | 1{neighbors ≥ τ} | hidden random | both | — |

A delay-d world is `own` with a shift-register machine (H = 2^d): already inside
the class, so not a separate twist. Which twists earn a place is decided by
`twists.py`, not by taste: certify rate (criterion 1) and the distinctness
matrix D[class i][world j] (criterion 2; row `own` = memorisation control).

## Key definitions

- **Dynamics**: `v' = birth/survive[h][neighbor count]`, `h' = h_next[h][own v]`, h0=0.
- **err(0)** is the best *order-1 3×3* visible predictor (not "best visible-only":
  wider windows or deeper history recover part of h).
- **err(k) curve** is the difficulty axis: gap dying at k=1 = two-state cells;
  gap surviving k=8 = hard worlds.
- **Degenerate**: effective_H < 2 by occupancy (≥5%), or occupied rule tables
  disagreeing on < 2% of occurring patterns. ~20% of sampled worlds; the k=0
  gap alone would silently include some of these.

## Design notes for Phase 1

- The observation interface MUST expose per-cell time series (frame-by-frame
  grids), else h is undiscoverable by construction — unfair, not hard.
- Start human-learnability checks at H=2.
- The k=0 predictor's held-out error doubles as the "laws must beat the
  obvious model" term in the court's score.
- Next: interaction protocol (observe/set/reset, budgeted), law grammar, court;
  scripted baseline agents before any LLM.
