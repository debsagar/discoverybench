# Benchmark brief for outside review (18 Sep 2026)

You are reviewing a benchmark design in progress. Be critical. We want holes found, not encouragement.

## 1. What we are trying to build

A benchmark that tests whether a language-model agent can do discovery: enter an unknown world, run experiments, and hand in a theory of how it works. We generate the worlds, so we own the true rules and can check any theory exactly.

Goals, in order:
1. A benchmark the strongest current models do badly on. Our hypothesis is that models are weak at open-ended discovery, specifically at exploring, noticing they are wrong, and rebuilding their story.
2. One clear headline percentage.
3. Longer term, the same environment should be usable to train the skill. We have no training compute, so this is only a design lens. The paper is a benchmark paper. We test small models first, then frontier models.

Constraint from the project owner: it must stay intuitive. It has drifted toward being too theoretical.

## 2. What exists today

Worlds are Conway-Life-style grids with one twist. Every cell carries a hidden dial with 2 or 3 positions. The dial picks which birth/survival rulebook that cell uses this tick. Then the dial turns, based on one bit: either "was I on" or "did I have at least N neighbours". The agent sees only on/off cells, never dials. All dials start at 0. Everything is deterministic and seeded. 23 tests pass, including one showing plain Life is a special case.

Supporting code: a brute-force "theorist" that tries every possible dial gearbox (729 for 3 positions) and fits rule tables by counting; a set of scripted pokes (paint or clear a block mid-run with dials carried over); and a pilot harness that ran two models.

Measured facts:
- A predictor that sees only the visible grid, even with 8 frames of history, gets up to 25% of cells wrong. So the dial matters.
- After 64 watched frames, about half of worlds still have 30 to 50 rule sets that fit with zero error.
- On our example world (seed 34), 47 rule sets survive watching. A mid-run "paint a 4x4 block" poke eliminates 6 of them. A "clear" poke eliminates 0. Three other pokes eliminate all 47, but that result is an artifact (see 3.4).

## 3. Problems we have found

3.1 The exam tests the wrong thing. The pilot asks the model to hand-draw the next 32x32 frame (1,024 cells). In 8 of 10 recorded runs (Gemini 2.5 Flash and GPT-5.4, 5 worlds each) the model did worse than copying the previous frame. That includes the control world with no hidden state. So a bad score cannot separate "missed the hidden state" from "cannot simulate a grid by hand". The owner never wanted this exam. It crept in from how prediction benchmarks usually work.

3.2 The score that matters is missing. Models were also meant to submit a runnable rule set. Its score is empty in all 10 result files.

3.3 Agents cannot intervene. The pilot only lets the agent choose a starting picture and watch. Pokes exist only in our own audit script. The core idea has never been tried on a model.

3.4 The submit format leaks the answer. It asks for "number of hidden states", "what drives the hidden state (own / count / clock)" and the tables. The agent never has to think of hidden state by itself.

3.5 Surviving-theory counts are inflated. Renaming dial positions gives a "different" theory that behaves identically. Rule-table entries never seen in the data are filled with zero, so pokes that start from unusual pictures kill every theory, including the one with the correct gearbox. The existing test misses this because it only compares gearboxes.

3.6 No proof each world is solvable within the experiment budget.

3.7 Our efficiency measure compares a smart poker to a random poker. Existing active-learning theory says that is not enough; you also need the best fixed plan and the best adaptive plan to claim that thinking helped. We have also not established that any of this is novel. Related work we know of: CellARC (passive cellular-automaton rule inference), Agentic Automata Learning (agents query a hidden finite-state machine, June 2026), AutumnBench/WorldTest (43 interactive grid worlds, humans beat frontier models), ARC-AGI-3 (interactive games scored by action efficiency; frontier scores went from under 1% to about 60% in six months), NewtonBench (altered physics laws, experiment budget).

3.8 The hidden dial is small. One bit in, per-cell, fully reconstructible from visible history, and brute-forceable. If the agent has a code sandbox, it can solve it the way our theorist does.

3.9 Small samples. Six exam questions per world, one run per model, no error bars, unreadable replies silently scored as the lazy baseline. Replies are about 9,500 characters each, heavy for small models.

3.10 A deeper worry. "Add a hidden variable per cell" is a patching move, like the ether. Real breakthroughs often come from stepping back and changing the framing (Einstein and Lorentz fit the same data; Einstein dropped an assumption and the patches vanished). Our grader checks behaviour only, so an ugly patched theory scores the same as the simple right one.

## 4. Proposed redesign: "Life with a secret"

The agent is told only: "This is a 12x12 grid world. Work out how it behaves. Hand in a program that steps it."

Three actions:
- Run: draw a starting picture, choose the number of ticks, get the movie.
- Poke: reopen an earlier run at a chosen tick, change some cells, continue. Hidden state carries over.
- Submit: a small program taking the grid plus free-form memory and returning the next grid plus memory. Nothing in the format hints that memory is needed.

Budget: 20 runs or pokes, 3 submits. A failed submit returns one movie where the program was wrong.

Grading: the program is run against the truth on 50 fresh situations, including pokes the agent never tried. Every frame must match. Headline = percent of worlds solved. Anchors: a random poker (expect near 0%) and a scripted scientist (expect near 100%, which doubles as the solvability proof).

Secondary measures: actions used; share of the possible efficiency gain captured (0 = random, 100 = best planner); whether the agent's next experiment after a failed submit goes after the counterexample; whether it ever introduces memory.

Secrets, one per world, not announced: none (control); tired cells (on two ticks running changes survival); crowd scars (once crowded, different rulebook forever); gossip (hidden state depends on neighbours' hidden state); seasons (global rulebook switches every few ticks); two countries (rules differ by region). The first three are the existing dial renamed.

Quality checks per world, behind the scenes: scripted scientist solves it within budget; a watcher who never pokes fails it.

Additions from the Einstein lens:
- Wrong-framing worlds. Example: a cell's neighbourhood reaches into the previous tick on one side. Seen as grid-plus-time it needs memory and exceptions; seen as one block of space and time it is a simple rule.
- The Lorentz task. Give an archive of movies plus a working but ugly theory (about 40 lines, several special cases). Ask for a simpler program that still passes, and one experiment where old and new disagree.
- Test far outside the explored range (bigger grids, extreme densities, long runs) so patched theories break and the right idea survives, without needing a judge of elegance.
- Some worlds solvable from the archive alone, with zero pokes.

## 5. Open questions we want your view on

1. Should the agent have a code sandbox while exploring? We lean yes, since that is how agents are used, but it makes small secrets brute-forceable.
2. Does returning a counterexample on a failed submit give too much away? Alternative: pass/fail only.
3. Is exact behavioural match on 50 situations the right bar, or too strict or too loose? How should equivalent-but-differently-written programs and edge cases be handled?
4. Is "percent of worlds solved" a sound headline, and what should the second number be?
5. Are the six secrets different enough from each other and from prior benchmarks to support a claim about discovery in general, or is this just a harder cellular-automaton puzzle?
6. Is the wrong-framing / Lorentz task fair and gradable, or is it a planted trick?
7. What would make this saturate within six months the way ARC-AGI-3 appears to be doing, and how do we design against that?
8. What are we missing from the literature on active learning, experimental design, program synthesis and scientific-discovery benchmarks?
9. Where is this still too theoretical or unintuitive?
