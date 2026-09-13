# Codebase map — what owns what

Data flows left to right. Nothing to the right of `sim.py` may read ground-truth `h`.

```
spec.py ──► drivers.py ──► sim.py ──► floor.py ─────────┐
 (world)     (twist:       (ground     (err(k), oracle,   │
              signal d,     truth)      degeneracy)       ▼
              h0 field)       │                        certify.py ──► certificates.json
                              ├──► enumerator.py ──►     ▲   (Gate B verdict per world)
                              │     (null family,        │
                              │      data pools)   ──► gate_a.py   (score-vs-budget curves)
                              └──► theorist.py   ──►  gate_a2.py  (class cost, extrapolation)
                                    (induction)   ──►  twists.py   (criteria 1 & 2 → twist_study.json)
                                        │
                                        └──► pilot.py (exam) ◄── run_pilot.py (LLM driver)
test_wmi.py pins one claim per test across all of the above.
```

| file | owns | must NOT |
|---|---|---|
| `spec.py` | `WorldSpec` (tables, machine, `driver`, `param`, `h0`), `TWISTS`, `sample_spec(seed, H, twist)`. Baseline `own` keeps the legacy seed stream. | simulate |
| `drivers.py` | `signal(driver, param, v, count, t)` — the ONE definition of every twist; `h0_field(spec, rng, shape)` | know tables |
| `sim.py` | `neighbor_counts`, `step(spec, v, h, t)`, `rollout`, `random_state(rng, spec, n)` | fit anything |
| `floor.py` | `patterns`, `markov_floor` → err(k), err_h oracle, occupancy/effective_H/rule_disagreement | theorise |
| `enumerator.py` | `train_pool`, `held_out`, `feats`, `enumerator_err(chunks, held, k)` for k ∈ `KS=(0,1,2,8,"t")`, `persistence_err` | posit a latent |
| `theorist.py` | `machines`, `h_fields`, `fit_tables` (hard-EM when `infer`), `infer_h0`, `held_err`, `best_in_class`, `theorist_err(chunks, held, spec)`, `classes`, `select` (MDL) | read true h |
| `certify.py` | `desc_bits`, `certify(spec, budget)`, thresholds `MIN_ENUM_RES` `MIN_ENUM_FRAC` `MAX_THEORY_RES` | choose twists |
| `gate_a.py` / `gate_a2.py` / `experiment.py` | experiments only (loops + printing + JSON) | define agents |
| `twists.py` | criterion 1 (certify rate per twist), criterion 2 (distinctness matrix D) | reusable logic |
| `active.py` | feasibility of the active loop: `hypotheses`, `survivors` (zero-error theories after passive budget), `POKES`, `outcome` (h carried through a mid-run edit), `audit` → `active_<twist>.json` | define agents |
| `pilot.py` | exam: `Session`, `make_probes`, prompts, `score_predictions`, `score_declaration`, `eval_submitted_model` (reuses `theorist.h_fields`/`infer_h0` + `sim.step`) | its own h reconstruction |
| `run_pilot.py` | LLM tool loop, WORLDS list, result files | scoring |

## Debug routes

| symptom | look in |
|---|---|
| a twist behaves differently in sim vs theorist | `drivers.signal` — both call it; if they differ, the bug is a wrong `t` or `count` passed in |
| theorist err > 0 with the class given | `theorist.best_in_class` tie-break (two machines with equal train err → non-identifiable at this budget; raise budget before suspecting code) |
| `own_h0` slow | `theorist.fit_tables` EM rounds × H candidates × machines; `_counts` cache must be hitting (key = address+shape+checksum) |
| world certified but LLM/enumerator numbers look off | `enumerator.feats` context bits (k history above bit 9; `"t"` uses `t mod T`) |
| exam scores true machine ≠ 0 | `pilot.eval_submitted_model` builds a `WorldSpec` then `step(…, t=8)`; check `h0` mode and `param` parsed |
| seed 21 stopped being the flagship world | `spec.sample_spec` rng seeding: `own` must use `default_rng(seed)` |
| new twist | add to `drivers.signal` + `spec.TWISTS` (+ `PARAMS` in `twists.py`); tests parametrised on `TWISTS` pick it up |

Run: `python3 -m pytest test_wmi.py -q` (~1 min). Complexity: `radon cc -s -n C *.py` (only pre-existing pilot/experiment loops are C).
