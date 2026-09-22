# Hidden-dial Life (world-model induction, phase 0)

**Retired:** 2026-09-22
**Lived:** 2026-09-01 to 2026-09-22
**Replaced by:** the layered "balls on a grid" world (design in progress, not yet in the repo)

## The idea, in the words it was proposed in
A benchmark for whether an AI can do science, not just predict. Small grid worlds like Conway's Life, but every cell has a hidden switch (the "dial") that changes which rulebook it uses; the dial turns based on one bit of the cell's own past. Watching alone cannot tell you which of several simple explanations is true. You have to poke the world and ask the right question. Score how many pokes a model needs versus a random guesser. We own the ground truth so every answer is checkable. (User, 2026-09-02 and 2026-09-15.)

## What was built
- `spec.py` world definition: per-dial birth/survive tables, dial gearbox, seeded sampler.
- `sim.py` the simulator; owns ground truth; plain Life falls out as a special case.
- `drivers.py` what the dial listens to: own state, crowding (count >= tau), or a global clock.
- `theorist.py` a script that tries every gearbox (H^(2H)) and fits rule tables by counting; the "scripted scientist" of this phase.
- `enumerator.py`, `floor.py` visible-only lookup-table predictors with k frames of history; the "watcher who never thinks about hidden state".
- `certify.py`, `gate_a.py`, `gate_a2.py`, `twists.py` world-quality checks: keep a world only if the counting fitter is near zero error and the lookup table is not.
- `active.py` after 64 watched frames, list every gearbox+table with zero error; then apply five scripted pokes and count which candidates predict differently from the truth.
- `pilot.py`, `run_pilot.py` LLM harness: 6 budgeted observe() calls, then an exam. `pilot_results/`, `pilot_results_v2/` are the recorded runs.
- `experiment.py`, `test_wmi.py` (23 tests, pass from this directory), `MAP.md`, `PHASE0-README.md`, `docs/` (plans, research notes, the 2026-09-18 review brief).

## What it produced
- World sampling, H in {2,3}, 100 seeds: 25 kept, 35 solvable by a lookup table, 40 rejected as dead/frozen/degenerate. `certificates.json`.
- By twist (20 worlds each): own 8 kept / 7 lookup-solvable / 5 rejected; count 5/3/12; clock 2/7/11; own with random start dials 5/5/7 plus 3 that no fitter solved; count with random start dials 10/4/5 plus 1. `twist_study.json`.
- Seed 34 (own, H=3) after 64 watched frames: 47 candidate theories with zero error. Mid-run "paint a 4x4 block, dials carried" kills 6; mid-run "clear a block" kills 0; "block from empty", "sparse soup", "dense soup" each kill all 47. `active_own.log`. The 47-kill pokes start from pictures the watched soups never produce, so they hit rule entries the fitter had filled with zeros; they kill the correct gearbox too (log event 2026-09-13, `docs/research/2026-09-13-certifiable-experiments-evidence.md`).
- LLM pilot, hand-draw-tick-9 exam, 5 worlds x 2 models (gemini-2.5-flash, gpt-5.4), error fraction of cells vs copy-previous-frame: v1 model worse than copying in 8 of 10 runs; v2 in 8 of 10. On the no-dial control world H1 s1000: v1 0.4806 and 0.4512 vs copy 0.4325. `pilot_results/`, `pilot_results_v2/`. The runnable-rulebook score is absent in every file.
- Both models declared that hidden state exists on 4 of 4 dial worlds each; gpt-5.4 guessed the right number of dial positions on 1 of 4 (seed 29). `pilot_results/*.json`, field `declaration`.

## Why it was retired
Three reasons, in order of weight. (1) The exam measured the wrong thing: models were asked to hand-simulate 1,024 cells, and lost to copy-the-last-frame even on the control world, so scores could not separate "missed the hidden state" from "cannot simulate by hand". The user never asked for this exam (2026-09-18: "idk from where we got the idea of simulate a big grid by hand, i never wanted this"). (2) Life has no conserved quantity and no simple coarse law, so it has no natural layers; a shallow theory never "works then breaks", it is just wrong or right (literature sweep 2026-09-18, `../../research/literature/02-substrates.md`). (3) A single small per-cell switch with one input bit is brute-forceable by any agent with a code sandbox (729 gearboxes at H=3), so it captures almost none of what makes real discovery hard.

## World beliefs
- [kept] On these worlds, a predictor that sees only the visible grid, even with 8 frames of history, still gets a large fraction of cells wrong, so the hidden switch is real and matters.
    how we know: `certificates.json` field `headroom` (lookup-table error minus counting-fitter error), e.g. seed 1 H=2 headroom 0.3862; `PHASE0-README.md` quotes up to 25%.
    where it came from: measured by the assistant; user asked for the check.
    would be wrong if: a k=8 lookup table reached the fitter's error on a kept world.
    scope: 32x32 toroidal hidden-switch Life, H in {2,3}, 64 watched frames. Says nothing about other worlds.
- [kept] Watching 64 frames of random soups leaves many theories tied at zero error; only an intervention that creates situations soups do not produce can split them, and interventions from unnatural starting pictures split them for the wrong reason (untested rule entries).
    how we know: `active_own.log` seed 34: 47 alive; fill kills 6, clear 0, block/sparse/dense 47 each; the 47-kill artifact is documented in `docs/research/2026-09-13-certifiable-experiments-evidence.md`.
    where it came from: measured; the artifact was found by an audit the user requested.
    would be wrong if: dedup by behaviour plus unknown-marking of unseen entries left the fill poke killing none.
    scope: seed 34 own H=3 only; other seeds in the log show 0 kills for every poke.
- [kept] Counting a smart poker's pokes against a random poker's does not prove thinking helped; the best fixed plan and best adaptive plan are also needed.
    how we know: prior-art review, log event 2026-09-13 (Nowak, Hanneke, adaptive vs fixed designs), `docs/research/2026-09-13-contribution-assessment.md`.
    where it came from: the assistant's literature check, prompted by the user asking for a contribution assessment.
    would be wrong if: a source showed smart-vs-random alone is accepted as evidence of adaptive advantage.
    scope: the scoring argument, not any world.
- [dead] Models were fairly tested by hand-drawing the next 32x32 frame.
    how we know: worse than copy-previous-frame in 8 of 10 runs in both v1 and v2, including the no-dial control. `pilot_results/`, `pilot_results_v2/`.
    where it came from: I assumed it (nobody asked); copied from how prediction benchmarks test.
    would be wrong if: a model beat the copy baseline on the control world.
    scope: 6 questions per world, 2 models, 5 worlds.
- [dead] "Counting fitter fits, lookup table does not" means a world needs a theory.
    how we know: two thirds of kept own worlds became lookup-solvable given more frames; the certificate measured cost to memorise, not need for a theory. Log 2026-09-02T10:15 decision; `PHASE0-README.md`.
    where it came from: the assistant proposed the certificate; user accepted then retired it.
    would be wrong if: kept worlds stayed lookup-unsolvable at any budget.
    scope: own twist, H=3, budgets up to 64 frames.
- [open] A mid-run poke with hidden state carried over is the right intervention primitive.
    how we know: only the two mid-run pokes (fill, clear) avoid the untested-entry artifact; never tried on a model.
    where it came from: assistant inference from the seed-34 audit.
    would be wrong if: models given this poke did no better than watchers.
    scope: untested on any agent.

## Method beliefs
- [kept] Environments must be proven to carry signal before any model sees them: a scripted scientist must solve each world within the experiment budget, and an agent that only watches and never pokes must fail it. Worlds that fail either check are dropped.
    how we know: this phase's checks did the first half (counting fitter vs lookup table) and it still produced a pilot that measured nothing; the user stated the two-sided form on 2026-09-18.
    where it came from: user's core intuition, stated 2026-09-02 ("search vs budget") and sharpened 2026-09-18.
    would be wrong if: a world passing both checks still produced scores indistinguishable from chance for every agent.
    scope: any generated world.
- [kept] A single small hidden switch captures almost none of real discovery. Real discovery is a sequence: a shallow theory fits, then fails in a rarer reachable regime, then gets rebuilt. Worlds need layers, which come from conserved quantities plus a scale the agent can push, not from bolted-on tricks.
    how we know: phase 0 had one layer and was brute-forceable; literature sweep 2026-09-18 (`../../research/literature/01..05`) found conserved-quantity substrates have documented regime-limited laws and Life does not.
    where it came from: user's step-back on 2026-09-18 ("think from Einstein's perspective"; "worlds need layers resonated"); literature gathered by Sonnet agents, not independently verified by the assistant.
    would be wrong if: a one-layer world turned out to separate strong from weak discoverers as well as a layered one.
    scope: design principle; the layered world is not built yet.
- [kept] Grade only the final submitted world model by running it against the truth on situations the agent never saw, including interventions. Never grade reasoning steps. A patched theory may live until nature breaks it.
    how we know: user decision 2026-09-18, memory file benchmark-design-principles.
    where it came from: user, after outside review.
    would be wrong if: behaviour-only grading let a memoriser pass on held-out interventions.
    scope: the grading contract.
- [kept] This is an evaluation benchmark only, with no training compute, but built with RL-environment practice (procedural generation, exact simulator truth, held-out world families, anti-overfitting, per-step checkable reward) so it can be ported to an RL environment later. The paper must not mention RL.
    how we know: user statements 2026-09-18.
    where it came from: user.
    would be wrong if: n/a, it is a constraint.
    scope: whole project.
- [kept] Headline score is percent of worlds solved; second number is recovery (of worlds where the first submit failed, how many were eventually solved) or experiment efficiency.
    how we know: user decision 2026-09-18.
    where it came from: user, after outside review.
    would be wrong if: solved-percent saturated while recovery still separated models, or vice versa.
    scope: scoring.
- [kept] The agent gets a code sandbox. If brute force solves a world, the world is too weak.
    how we know: user decision 2026-09-18; phase 0's 729-gearbox search is the cautionary case.
    where it came from: user.
    would be wrong if: n/a, it is a constraint.
    scope: interface.
- [kept] Keep the benchmark intuitive: every mechanism gets a plain name (a watcher who never pokes, a scripted scientist), never a label.
    how we know: user 2026-09-18 ("the benchmark became too theoretical and less intuitive").
    where it came from: user.
    scope: all writing.

## Assumptions we made without being asked
- The hand-drawn tick-9 exam. Crept in from prediction-benchmark habit. Cost: two pilot rounds (20 runs) that could not measure discovery.
- The submit format that names "n_hidden", "driver", "h_next": it told the agent the shape of the answer. Crept in from wanting exact parsing. Cost: the agent never had to think of hidden state itself.
- The "certified" label and description-length scoring as headline concepts. Crept in from wanting a proof of difficulty. Cost: two weeks on a certificate that measured memorisation cost, and a vocabulary the user found unintuitive.

## How to run it again
From this directory:
```
python3 -m pytest test_wmi.py -q        # 23 passed in 57s on 2026-09-22
python3 active.py own 20                # rewrites active_own.json here
python3 certify.py
python3 run_pilot.py --models google/gemini-2.5-flash   # needs OPENROUTER_API_KEY; imports /data/MathBench/providers.py
```
`show.py` (the ASCII walkthrough) lived only in a session scratchpad and is not here.
