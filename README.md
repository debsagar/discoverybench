# discoverybench

**Status (2026-09-22):** the hidden-dial Life phase is archived under `attic/` with its results and standing beliefs. The next world (layered, conserved balls on a grid) is being designed. `ideas/` holds the owner's intuitions, `research/` the literature.

A benchmark for **world-model induction**: can an agent watch a small hidden-rule
world, form a theory of it, and prove the theory by running the right experiment?

## The world

A 2-D cellular automaton like Conway's Life, except every cell carries a hidden
"dial" (`h` in `0..H-1`). The dial picks which birth/survive row applies to the cell,
and the dial itself turns according to what the cell (or its neighbourhood) just did.
The agent sees only the on/off grid, never the dial.

```
visible:  v' = birth/survive[h][neighbour count]
hidden:   h' = machine[h][signal]      signal = own v  ("own")  or  1{count >= tau}  ("count")
```

Everything is generated from a seed, so the ground truth is owned and exact.

## What we found so far (archived in `attic/2026-09-22-hidden-dial-life`)

1. **The hidden dial is real.** A visible-only predictor with 8 frames of history
   still mispredicts up to 25% of cells on many worlds; given the true dial it is exact.
2. **"Hard to memorise" is not "needs a theory".** The first certificate
   (theory fits, lookup table does not) mostly measured sample cost. Retired.
3. **Passive watching leaves theories tied; a poke breaks the tie.** After 64 frames,
   roughly half the worlds still have 30-50 zero-error rival theories. Painting a
   4x4 block mid-run and continuing kills nearly all of them. That is the benchmark's
   new target: observe, hypothesise, intervene, revise.

## Layout

```
attic/2026-09-22-hidden-dial-life/
  spec.py       world definition + seeded sampler
  drivers.py    the hidden-dial signal (one definition shared by simulator and theorist)
  sim.py        ground-truth simulator (reduces to Life at H=1)
  floor.py      how much history a visible-only predictor needs
  enumerator.py lookup-table baselines
  theorist.py   scripted theorist: enumerate dial machines, fit tables, MDL selection
  certify.py    old per-world certificate (kept for reference)
  active.py     active-loop feasibility: survivors after passive watching, pokes, kills
  pilot.py / run_pilot.py   LLM exam (observe -> predict -> declare a model)
  test_wmi.py   one test per claim
  MAP.md        who owns what, debug routes
wmi/docs/plans  design notes
```

## Run

```
cd attic/2026-09-22-hidden-dial-life
python3 -m pytest test_wmi.py -q     # ~1-2 min
python3 active.py own 20             # which worlds are passively ambiguous but poke-separable
python3 certify.py                   # old certificate
```

`run_pilot.py` needs `OPENROUTER_API_KEY` in the environment.
