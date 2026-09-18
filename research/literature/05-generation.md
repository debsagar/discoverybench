# Procedurally Generated Environments With Guarantees

Angle: how to build a world generator with a "depth" knob that produces endless
fresh worlds, guarantees solvability within a budget, resists brute-force
search by an agent with a code sandbox, and resists the agent learning our
generator's grammar instead of the underlying world.

Rules followed per `_brief.md`: only claims from sources I opened; inference
flagged explicitly; sources have title/authors/year/URL.

---

## 1. Procgen: procedural generation as an anti-overfitting device

**Leveraging Procedural Generation to Benchmark Reinforcement Learning.**
Cobbe, Hesse, Hilton, Schulman (OpenAI), ICML 2020. arXiv:1912.01588.
https://arxiv.org/abs/1912.01588v2 (full text via
https://ar5iv.labs.arxiv.org/html/1912.01588)

What it says: 16 procedurally generated game-like environments, one level
sampled per episode, so an agent cannot memorize fixed trajectories the way it
can on the Arcade Learning Environment. Their headline empirical result:
agents trained on a *fixed, finite* set of levels can look competent during
training while test performance shows "the agents have in fact learned almost
nothing about the underlying level distribution" — i.e. large in-distribution
training performance is not evidence the agent learned the generative rule.
Quantitatively, they find agents need on the order of **10,000 levels** to
close most of the generalization gap, but recommend **500 levels** as a
practical benchmark threshold ("near the region where generalization begins
to take effect"). Why it matters for us: this is the sharpest documented case
of "environment looks solved, agent has memorized a shortcut," and gives a
concrete lower bound on how large a "training slice" of a generator's output
must be before near-perfect scores mean anything at all — directly relevant
to sizing any public/practice slice of our world generator versus its private
tail.

## 2. XLand-MiniGrid: compositional rule+goal grammar at scale

**XLand-MiniGrid: Scalable Meta-Reinforcement Learning Environments in JAX.**
Nikulin et al., NeurIPS 2024 Datasets & Benchmarks. arXiv:2312.12044.
https://arxiv.org/abs/2312.12044

What it says (abstract-level; I could not get full text through the fetcher):
combines the compositional rule/goal system of DeepMind's XLand ("keys open
doors of the same color," "go to the blue box") with MiniGrid's minimalism.
Rules and goals compose combinatorially to yield benchmarks with **millions
to ~10^8 distinct tasks**, run at tens of millions of steps/sec on GPU/TPU.
My inference (not verified from full text): a combinatorial rule grammar is
exactly the kind of structure an agent — or an LLM agent with a code sandbox
— can reverse-engineer once it has seen enough instances, because the
*surface* variety (huge task count) sits on top of a *small, fixed* generative
grammar (few rule types, few goal types). Large task count is not the same as
resistance to grammar induction. This is a warning for our own generator: if
depth is implemented as "more rules from the same small vocabulary," a
sandboxed agent can enumerate the vocabulary directly from the generator's
observable behavior (or from cracking the seed) rather than by experimenting
in the world.

## 3. Craftax: benchmarks fail by being too slow or too shallow, not both

**Craftax: A Lightning-Fast Benchmark for Open-Ended Reinforcement Learning.**
Matthews, Beukman, Lu, Foerster et al., 2024. arXiv:2402.16801.
https://arxiv.org/abs/2402.16801

What it says: prior open-ended benchmarks split into two failure modes —
too slow to iterate on (Crafter, NetHack, Minecraft) or not complex enough to
be a real challenge (MiniGrid, Procgen). Craftax is a JAX rewrite achieving
up to 250x speedup over Crafter, and states that solving it "requires deep
exploration, long-term planning and memory, as well as continual adaptation
to novel situations as more of the world is discovered." It further reports
that existing global/episodic exploration methods *and* unsupervised
environment design methods "fail to make material progress" on the full
benchmark. I could not extract the exact basic/intermediate/advanced/very
advanced achievement tiers or reward counts from the fetchable text (search
snippets mention 1/3/5/8 reward tiers respectively; flagged as
**unverified**, sourced only from search-result summary, not from text I
opened myself).

Why it matters: it is direct evidence for our depth-knob thesis at the
systems level — a world needs enough combinatorial depth (crafting/tech
tree, memory requirements) that shallow strategies plateau, and current
autocurriculum methods (UED) don't automatically solve this; depth needs to
be a first-class knob in the generator, not something UED discovers for free.

## 4. Kinetix: an open-ended physics generator as the "depth via composition" case study

**Kinetix: Investigating the Training of General Agents through Open-Ended
Physics-Based Control Tasks.** Matthews, Beukman, Ellis, et al., ICLR 2025
(oral). arXiv:2410.23208. http://arxiv.org/abs/2410.23208v1

What it says: procedurally generates tens of millions of 2D physics tasks
(mazes, manipulation, locomotion, classic-control-style tasks) inside one
unified physics representation, using a custom hardware-accelerated engine
(Jax2D) for cheap simulation. Trained general agents "zero-shot solve unseen
human-designed environments," i.e. skill transfers out of the generator's own
distribution into hand-authored tasks it never saw. Why it matters: this is
the strongest evidence in this batch that a *single underlying physics
substrate* (few fixed rules: rigid bodies, joints, forces) can support
open-ended task generation without the agent's competence being just "learned
the generator's grammar" — because success is validated against
human-authored out-of-distribution tasks, not just more generator samples.
This argues for building our depth knob on a small number of composable
*physical/causal primitives* whose interactions produce genuinely novel
regimes, rather than on a combinatorial rule-list grammar (contrast with
XLand-MiniGrid's rule/goal lists, §2).

## 5. Unsupervised Environment Design (UED): PAIRED, PLR, ACCEL — regret as an automatic difficulty knob

- **PAIRED** (Dennis et al., NeurIPS 2020; cited via secondary sources found
  in this search, not independently opened — **flagged as unverified from
  primary text**): a teacher network generates levels to maximize the
  performance gap ("regret") between a protagonist and an antagonist policy
  on the same level, which in theory targets levels that are learnable but
  not yet solved, avoiding both trivial and unsolvable levels.
- **Prioritized Level Replay (PLR)**: curates a replay buffer of
  high-regret levels; at each episode chooses between fresh domain-randomized
  levels and revisiting high-regret ones from the buffer.
- **ACCEL — Evolving Curricula with Regret-Based Environment Design.**
  Parker-Holder, Jiang, Dennis, et al., 2022. arXiv:2203.01302.
  https://arxiv.org/abs/2203.01302 (fetched via
  https://arxiv.org/pdf/2203.01302). ACCEL extends PLR by *mutating* the
  most recent high-regret levels (small edits: move an object, tweak
  dimensions) rather than only sampling fresh random levels, so search stays
  in the neighborhood of levels that are hard-but-learnable. Regret here is
  operationalized as the gap between an agent's realized value and an
  estimate of the level's achievable value; as the agent improves, regret on
  old levels drops and the mutation process is pushed toward new levels at
  the frontier of capability, producing a curriculum of increasing difficulty
  "for free" from the interaction of (agent competence) x (regret-seeking
  search), without hand-authored difficulty tiers.

Why it matters for the depth knob: regret-based UED is the closest existing
mechanism to "a generator that automatically finds the next regime where the
current theory fails," which is exactly our depth-knob requirement. But
Craftax's finding (§3) that UED methods "fail to make material progress" on
a genuinely deep benchmark is an important caution: regret-driven curricula
work well for finding locally-harder variants of a fixed task family, but
don't by themselves manufacture qualitatively new regimes (new physics,
new causal structure) — that structural depth has to be designed into the
generator's primitives, not left for a regret signal to discover.

## 6. Guaranteed solvability in procedural content generation

**General finding** (drawn from multiple PCG survey/technique papers
surfaced in search — see below): "unsolvable levels are almost inevitable"
under purely learned/generative approaches (e.g. GAN- or diffusion-based
level generators), which motivates two families of fixes documented in the
PCG literature:

1. **Generate-and-repair**: generate freely, then run a solver/repair pass
   that edits the level until a completability check passes.
2. **Solvable-by-construction**: build the level and a certificate of its
   solvability *simultaneously* — e.g. constraint-based generators that
   emit a reference solution/playthrough alongside the level, or fitness
   functions that only accept constructions satisfying reachability
   constraints, so unsolvable output is structurally impossible rather than
   filtered out after the fact.

Source pointers (surfaced via search, summaries only — **not independently
opened in full, flagged as secondary attribution**): work attributed to
Font et al. on fitness-based guaranteed solvability "by construction," and to
Nelson & Smith / Cooper on constraint-based generators that emit a reference
solution alongside the level. I was not able to open primary PDFs for these
within budget; treat as leads to verify, not confirmed claims.

**Constraint Satisfaction Problems (CSPs) as the general framework** for PCG
solvability guarantees — multiple sources describe CSP formulations as the
standard way to encode "must have a path from start to goal" or "must have
coherent terrain transitions" as generation-time constraints rather than
post-hoc tests.

Why it matters: for our generator, "solvable within a budget" should be a
generation-time invariant (approach 2), not a post-hoc filter, because a
post-hoc filter (approach 1) still requires *some* generate-and-test pass
that an agent with a code sandbox could in principle replicate (see §7) —
if we can construct the solution certificate for free during generation, we
never need to reveal that a search procedure exists at all.

## 7. Contamination, saturation, and holding out — ARC-AGI-3

**ARC-AGI-3: A New Challenge for Frontier Agentic Intelligence.**
ARC Prize team, 2026 (v.). arXiv:2603.24621. https://arxiv.org/abs/2603.24621
(details cross-checked against search-result summaries of the arXiv abstract
and arcprize.org/arc-agi/3 — full text not independently opened, so figures
below are **flagged as moderate-confidence, drawn from secondary summary**).

What it (reportedly) says: ARC-AGI-1 is described as approaching saturation
(top models >90%), which is presented as the direct motivation for versions
2 and 3. ARC-AGI-3 flips the public/private ratio relative to v1/v2 — where
earlier versions had roughly 10:1 public:private tasks, v3 keeps only ~25
environments public and holds the large majority private/semi-private for
evaluation — and moves to *interactive*, turn-based environments specifically
because static, single-shot puzzle grids are more easily contaminated
(memorized from web-scraped copies) or attacked with synthetic-data shortcuts
than an environment the agent must explore and act inside. There is also a
noted contamination signal in ARC-AGI-2 evaluation: a frontier model's
chain-of-thought referenced ARC-specific color-mapping conventions without
being prompted, suggesting the benchmark's public examples had leaked into
training data.

Why it matters: (a) it's direct, recent evidence that even a benchmark
explicitly designed against memorization saturates once a large-enough public
surface accumulates online, and the fix that has actually been deployed is
"shrink the public surface, keep growing the private one, and prefer
interactive over static tasks" — validates our own instinct to keep the
generator (not fixed instances) as the thing we own, and to never publish a
large fixed corpus of solved worlds; (b) interactivity itself is treated as
an anti-contamination property, not just a difficulty property, because a
scraped static answer key is useless against a world an agent must probe.

**The Benchmark Lottery.** Dehghani, Tay, Gritsenko, et al. (Google Brain),
2021. arXiv:2107.07002. https://arxiv.org/abs/2107.07002 (full text via
https://ar5iv.labs.arxiv.org/html/2107.07002).

What it says: apparent algorithmic superiority is heavily confounded by which
tasks happen to be in a benchmark suite — their SuperGLUE analysis shows 6
different "top model" rankings depending on which 4-task subset of the suite
you look at, out of 70 possible subsets. They also describe "benchmark
statefulness": as a benchmark ages, accumulated community tricks and
repeated querying of the same test set erode its statistical validity,
independent of any data leakage. Recommendations: rigorous
problem/dataset/metric-selection guidelines, statistical-significance testing
across multiple splits, "living benchmarks" that keep evolving to outrun
accumulated overfitting, and standardized reporting beyond a single headline
number. Why it matters: this is a generalized, non-ML-specific version of
the same warning as ARC-AGI-3 — any *fixed* set of task families (even if
individually procedurally generated) will accumulate exploitable statefulness
over time as agents/researchers query it repeatedly; the fix has to be an
ever-expanding or continually-regenerated task family, not a one-time-built
large set.

## 8. Construct validity and measurement-theory critiques of AI benchmarks (2024-2026)

Representative recent papers (titles/URLs verified from search results;
full text not opened for all — flagged where so):

- **Can We Trust AI Benchmarks? An Interdisciplinary Review of Current
  Issues in AI Evaluation.** 2025. arXiv:2502.06559.
  https://arxiv.org/html/2502.06559v1 — reviews systemic issues across a
  large literature sample; reports that of ~445 benchmark papers reviewed
  (from ~46,000 screened, 2018-2024), only 16% used uncertainty estimates or
  statistical tests when comparing results, and flags "misaligned
  incentives, construct-validity failures, and gaming risks" as systemic
  (attributed to a parallel EU Joint Research Centre meta-review).
  **Not independently opened in full — summary only.**
- **Measuring what Matters: Construct Validity in Large Language Model
  Benchmarks.** 2025. arXiv:2511.04703. https://arxiv.org/abs/2511.04703 —
  argues benchmarks should justify their link to the abstract capability
  they claim to measure with the same rigor social-science measurement
  theory demands, not just report a number. **Abstract-level only.**
- **What AI Benchmarks Actually Measure: Adapting Convergent and
  Discriminant Validity to Interrogate Fifty-Six AI Benchmarks.** 2026.
  arXiv:2609.08812. https://arxiv.org/html/2609.08812 — applies
  convergent/discriminant validity (does the benchmark correlate with other
  measures of the same construct, and *not* correlate with measures of
  different constructs) to 56 existing benchmarks; reports that a large
  fraction (search summary said 27%) rely on convenience sampling or
  contested construct definitions. **Not independently opened — flagged.**

Why it matters for us: these are general warnings, not specific to
procedural generation, but they sharpen the requirement on our "submit a
program that simulates the world" design: grading exactness (does the
submitted program reproduce the world's outputs) is a *convergent-validity*
guarantee almost by construction — it is much harder to fake than a
benchmark that scores a natural-language explanation or a scalar reward,
because the construct being measured (does the agent's theory match the
world) is identical to the grading procedure. This is a genuine structural
advantage of our design relative to the critiques above, worth stating
explicitly rather than assuming.

---

## Direct answer to the key question: what goes wrong with a generator that has a depth knob, solvability guarantees, and resists both brute-force search and grammar-learning?

Synthesizing across sources (this section is my inference, built on the
findings above, not a quote from any one paper):

1. **Large task count ≠ resistant to enumeration.** XLand-MiniGrid shows you
   can get 10^8 tasks from a small compositional grammar of rules and goals.
   Cobbe et al.'s Procgen result shows the flip side: an agent can look
   fully competent on a *bounded* slice of generator output while having
   learned nothing about the underlying distribution — and closing that gap
   took ~10,000 levels' worth of exposure. Both point the same way: what
   resists brute-force/grammar-learning is not "how many task instances" but
   "how large/deep is the underlying generative vocabulary the agent has to
   invert," and a code-sandboxed agent will happily automate exactly the
   enumeration that a human researcher would do by hand. If our depth knob
   is implemented as more items in a fixed small rule vocabulary, a sandboxed
   agent can extract the vocabulary from a modest number of samples and stop
   experimenting in the world entirely.

2. **Kinetix's contrasting design — physical primitives, not a rule list —
   is the better template.** A small number of continuous, composable causal
   primitives (forces, constraints, thresholds) that combine combinatorially
   produces open-ended surface variety from genuine underlying complexity
   (state-space size, nonlinearity), which is much harder to invert by
   pattern-matching on generator outputs than a discrete rule/goal grammar
   is. This is the direction implied for a "depth knob": depth should mean
   "more composed primitives / higher-order interactions," analogous to
   Newtonian mechanics failing at relativistic speeds not because a new
   *rule* was added but because an existing primitive (velocity addition)
   stopped being linear.

3. **Solvability should be a certificate produced during generation, not a
   post-hoc filter.** The PCG literature's "solvable-by-construction"
   approaches (generate level + reference solution/playthrough together)
   avoid ever running a discoverable search procedure that an agent could
   replicate. A generate-and-repair approach, by contrast, implies a
   solvability-testing procedure exists and is potentially inferable/attackable.

4. **UED / regret-based curricula (PAIRED/PLR/ACCEL) find local difficulty
   automatically but do not manufacture new regimes.** Craftax's explicit
   finding that existing UED methods fail to make progress on a genuinely
   deep, long-horizon benchmark is the clearest warning: don't rely on a
   regret signal to produce qualitatively new physics/rules at greater
   depth — depth has to be authored into the generator's primitive
   composition rules, with regret-style search only used to calibrate
   difficulty *within* a depth level, not to invent new depth levels.

5. **Never publish a large fixed corpus; keep the public surface small and
   the generator itself as the only permanent asset.** ARC-AGI-3's response
   to saturation (shrink public set, grow private set, move to interactive
   tasks) and the Benchmark Lottery's warning about benchmark statefurness
   both argue that any fixed corpus — however large — degrades with reuse.
   Interactive, freshly-sampled-per-episode worlds (Procgen's core design
   choice) are the standing defense against both contamination and
   benchmark statefulness simultaneously.

---

## 5 concrete world-design ideas, each traceable to a source

1. **Build depth from a small set of composable causal/physical primitives
   (not a discrete rule/goal list), so that "going deeper" means composing
   primitives at higher order, the way relativistic corrections are Newtonian
   mechanics plus a higher-order term.** Traceable to Kinetix's physics
   substrate producing genuine open-ended transfer (arXiv:2410.23208),
   contrasted with XLand-MiniGrid's rule/goal combinatorics being more
   grammar-learnable (arXiv:2312.12044, my inference).

2. **Generate the solvability certificate (a reference trajectory/derivation)
   simultaneously with the world, never as a post-hoc solver pass.** Traceable
   to constraint-based / solvable-by-construction PCG methods (Font et al.,
   Nelson & Smith, Cooper, as surfaced via search of the PCG literature —
   flagged as secondary attribution, primary text not opened).

3. **Keep any public/practice slice of the generator's output small and
   explicitly signal that it undersamples the true distribution — size the
   "practice regime" using Procgen's finding that ~500 levels only barely
   trigger generalization and ~10,000 are needed to close the gap, i.e.
   expect agents to overfit hard on anything below that order of magnitude
   and design scoring accordingly.** Traceable to arXiv:1912.01588.

4. **Use regret-style search (PLR/ACCEL-style level mutation) only to tune
   difficulty within a fixed depth level — not as the mechanism that produces
   new depth levels — since Craftax shows current UED methods stall on
   genuinely deep, long-horizon tasks.** Traceable to arXiv:2203.01302 and
   arXiv:2402.16801.

5. **Never let a fixed corpus of generated worlds become the permanent
   asset; treat the generator itself, continually able to mint fresh
   instances, as the only thing that doesn't saturate or leak — and prefer
   interactive/probe-based tasks over static ones since interactivity is
   itself an anti-contamination property, not just a difficulty property.**
   Traceable to ARC-AGI-3's public/private ratio flip and shift to
   interactive tasks (arXiv:2603.24621, secondary-summary confidence) and to
   the Benchmark Lottery's "living benchmark" recommendation
   (arXiv:2107.07002).

## Strongest objections / warnings from the literature

- **Task count is not a defense.** Millions of generated tasks (XLand-
  MiniGrid) can still sit on a small, invertible grammar; don't equate
  "endless fresh worlds" with "resistant to reverse-engineering" (my
  inference from contrasting arXiv:2312.12044 and arXiv:1912.01588).
- **UED/regret search is not sufficient for structural depth.** Craftax
  reports that current UED methods materially fail on deep benchmarks —
  don't assume an automatic curriculum will discover new regimes for you
  (arXiv:2402.16801).
- **Guaranteed solvability is genuinely hard in general** — the PCG
  literature treats unsolvable output as "almost inevitable" without either
  careful by-construction design or a repair loop; there is no free lunch
  here (search-summary attribution to Font et al. et al., not independently
  verified).
- **Any fixed, sufficiently public benchmark saturates.** Both ARC-AGI-3's
  own history (v1 near-saturated) and the Benchmark Lottery's "benchmark
  statefulness" argument say that reuse itself, not just leakage, degrades
  a fixed evaluation set over time (arXiv:2603.24621 secondary,
  arXiv:2107.07002 primary).
- **Construct validity is a real, largely unresolved problem across the
  field** — a low bar (16% of reviewed papers used any statistical rigor)
  suggests our own benchmark should not assume its scoring is self-evidently
  meaningful just because it is exact; exactness of grading (matching a
  simulator) answers the *measurement* half of construct validity but not
  necessarily the *construct* half (whether "predicts this simulator" is the
  right proxy for "did real scientific discovery") (arXiv:2502.06559,
  arXiv:251104703 — summary-level attribution for both).

## Sources not independently opened (flagged, use with caution)

- PAIRED (Dennis et al. 2020) — description drawn from secondary search
  summaries, not primary text.
- Font et al. / Nelson & Smith / Cooper on solvable-by-construction PCG —
  drawn from a search-engine synthesis, not from primary PDFs opened here.
- ARC-AGI-3 numeric claims (25 public environments, public:private ratio) —
  drawn from search-result summaries of the abstract and arcprize.org, not
  from full text opened directly.
- Craftax's basic/intermediate/advanced/very-advanced tier counts (1/3/5/8
  rewards) — from search snippet only, PDF fetch failed to render as text.
- Several construct-validity papers (arXiv:2502.06559, 2511.04703,
  2609.08812) — abstract/summary level only.
