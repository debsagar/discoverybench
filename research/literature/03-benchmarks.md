# Existing AI benchmarks for scientific discovery / world-model induction (2023-2026)

Angle: survey existing discovery/world-model benchmarks against our design question —
does anyone build worlds with **nested regimes of validity** (a shallow theory that
works, then fails in a rarer reachable regime, forcing revision), or is every world a
single flat rule? What's the gap, what mistakes do authors admit?

Rule followed: every entry below is from a source I actually opened (WebSearch result
pages and, for the four flagged with "[fetched abstract]", the arXiv abstract page
itself via WebFetch). I did not have live PDF rendering for most of these in this pass —
claims are drawn from abstracts/search snippets, which is a real limitation noted per
entry. Anything I could not verify is marked **[unverified/inferred]**.

---

## Entries

### NewtonBench — arXiv 2510.07172 [fetched abstract]
Zhou et al. (HKUST/NVIDIA), ICLR 2026. https://arxiv.org/abs/2510.07172
- **World**: 324 scientific-law-discovery tasks across 12 physics domains. Laws are not
  the textbook ones but **counterfactual law shifts** — systematic alterations of
  canonical physical laws — generated to be scalable and memorization-resistant.
- **Agent actions**: probes a simulated system experimentally (can request a code
  interpreter to analyze collected data).
- **Submitted / graded**: the discovered law, checked against the (altered) ground truth.
- **Difficulty control**: system complexity (number of interacting variables) and
  observational noise level.
- **Memorization prevention**: the counterfactual-shift trick — the surface form looks
  like real physics but the actual constants/exponents are deliberately wrong, so an LLM
  cannot pattern-match to Newton's laws from pretraining.
- **Human baseline**: not reported in what I could access.
- **Layers?** No nested regimes — each task is a single altered law across its full
  domain, not "law A near the origin, law B far away." **Single flat (if disguised) rule
  per task.**
- **Scores/saturation**: "clear but fragile" capability that "degrades precipitously"
  with complexity; interesting failure mode — giving frontier models a code interpreter
  *hurt* the strongest models by triggering premature exploration→exploitation
  switching (they "satisfice" on a suboptimal fit rather than keep probing).

### DiscoveryWorld — arXiv 2406.06769
Ai2. https://arxiv.org/pdf/2406.06769
- **World**: a virtual environment (text/grid based) with 120 tasks spanning multiple
  scientific domains (e.g. simulated chemistry/biology/astronomy scenarios), each
  requiring the full loop: hypothesize → design experiment → run it → analyze → act.
- **Agent actions**: move around, take measurements, run experiments, use in-world tools.
- **Submitted / graded**: a decision/action based on the discovered principle, scored
  against an oracle answer key baked into each procedurally-varied task instance.
- **Difficulty control**: "normal" vs "challenge" difficulty tiers.
- **Memorization prevention** **[inferred, not directly confirmed]**: procedurally
  varied instances per task, but I did not verify a specific anti-memorization mechanism
  beyond task variation.
- **Human baseline**: yes — practicing human scientists complete essentially all tasks
  humans attempted, while leading agents fail ~80% at normal/challenge difficulty. This
  is one of the largest human/model gaps in the set.
- **Layers?** No evidence of nested-regime worlds; each task has one target discovery.
- **Scores**: ~20% success for best agents vs near-100% for humans — far from saturated.

### PhysGym — arXiv 2507.15550
NeurIPS 2025 D&B. https://arxiv.org/abs/2507.15550
- **World**: interactive physics simulations; agent designs its own experiments,
  gathers data sequentially under a query/resource budget, then states a hypothesis.
- **Distinctive feature**: the *level of prior knowledge* (variable names, units,
  context) is an explicit, controllable knob, specifically to separate genuine
  mechanistic inference from cued recall — a direct attack on the memorization problem.
- **Difficulty control**: prior-knowledge level + problem complexity are both dialed
  independently, which is more principled than most entries here.
- **Layers?** No indication of regime-nested physics; standard fixed laws with variable
  prior-knowledge occlusion, not depth-of-theory structure.
- **Human baseline / scores**: not captured from search snippets; flagged
  **[unverified]** pending a fuller read.

### BoxingGym — arXiv 2501.01540 [fetched abstract]
https://arxiv.org/abs/2501.01540
- **World**: 10 environments, each a generative probabilistic model from real science
  domains (psychology, ecology, etc.) — e.g., agents interact with a simulated
  behavioral/ecological process.
- **Agent actions**: proposes experiments (choosing what to measure/manipulate),
  collects simulated data, revises a model.
- **Submitted / graded**: two things — (1) experimental design quality, scored by
  **expected information gain (EIG)** against the true generative model (a genuinely
  principled, non-LLM-judge metric); (2) a natural-language model explanation, scored by
  whether a second agent can use it to predict held-out data, plus standard prediction
  error.
- **Difficulty control**: not explicit in what I read.
- **Memorization prevention**: environments are probabilistic generative models the
  agent must interrogate live, not lookup-able facts — but not designed specifically
  against memorization.
- **Human baseline**: not found.
- **Layers?** No nested regimes reported — single generative model per environment,
  revision loop is about narrowing parameters / model class, not escaping a shallow
  theory into a deeper one.
- **Scores**: GPT-4o-class models "struggle with both" design and discovery; augmenting
  with explicit statistical tooling didn't reliably help — an interesting parallel to
  NewtonBench's code-interpreter finding (extra scaffolding not obviously beneficial).

### SciGym — arXiv 2507.02083
Duan et al., NeurIPS 2025. https://arxiv.org/html/2507.02083, https://h4duan.github.io/scigym-benchmark/
- **World**: a "dry lab" of real systems-biology models (350 SBML models from
  BioModels), so the ground-truth mechanism is a genuine curated biological network of
  varying size/complexity (from a few species/reactions up to hundreds).
- **Agent actions**: perturbs the simulated system, writes Python to analyze resulting
  data, iterates hypotheses.
- **Submitted / graded**: presumably a reconstructed model/network compared to the
  source SBML — **[inferred]**, exact metric not confirmed from snippet.
- **Difficulty control**: model size/complexity (species/reaction count) is a natural
  ordinal knob since the corpus already spans small to large real networks.
- **Memorization prevention**: real SBML models could in principle be in pretraining
  data — this is a **plausible weakness the authors would need to address**; I did not
  find an explicit anti-leakage mechanism in the snippets. **[flag: unresolved]**
- **Layers?** No nested-validity-regime structure; single fixed network per task,
  though network complexity varies across the corpus.
- **Human baseline / scores**: only 6 frontier LLMs tested on 137 small systems reported;
  no human baseline found.

### AutumnBench / WorldTest — arXiv 2510.19788 [fetched abstract]
https://arxiv.org/abs/2510.19788
- **World**: 43 interactive grid-world environments (in the "Autumn" DSL family used
  in prior cognitive-science work on rule learning), each supporting multiple query
  types.
- **Protocol (WorldTest)**: the real contribution is methodological — separate a
  **reward-free interaction phase** from a **scored test phase in a different but
  related environment**, and query the *environment-level* structure (e.g. reachability,
  effect of an intervention, masked-frame prediction) rather than just next-frame
  prediction. This is architecture/representation-agnostic.
- **Agent actions**: free interaction during phase 1; answering environment-level
  queries during phase 2 (no further environment access implied).
- **Submitted / graded**: answers to 129 tasks across 3 query families (masked-frame
  prediction, planning, causal-dynamics prediction), graded against ground truth.
- **Difficulty control**: not detailed in the snippet — likely varies by environment
  design, not an explicit knob. **[unverified]**
- **Memorization prevention**: the test environment differs from the interaction
  environment ("different but related"), which is itself an anti-memorization /
  anti-overfitting design choice — you can't just memorize the exploration environment's
  answers.
- **Human baseline**: yes, and a strong one — 517 human participants vs. 3-5 frontier
  models; humans clearly win, and "scaling compute improves performance only in some
  environments but not others" (i.e. saturation/plateau is uneven across world types,
  which is itself informative about which mechanics are learnable by scale alone).
- **Layers?** No nested regimes-of-validity described — the "different but related"
  test environment is a transfer/generalization test, not a deeper-truth-underneath
  structure. Closest of the group to our idea structurally (train/test environment
  separation) but not the same axis (transfer vs. depth).

### ARC-AGI-3 — arXiv 2603.24621 [fetched abstract via search]
https://arxiv.org/abs/2603.24621
- **World**: novel, abstract, turn-based grid environments; no language, no external
  knowledge — pure "Core Knowledge" priors (object permanence, agentness, etc., as in
  ARC lineage).
- **Agent actions**: explore, infer implicit goals (never told the objective), build an
  internal dynamics model, plan action sequences.
- **Submitted / graded**: successful task completion (reaching an implicit goal state)
  within an environment; presumably scored by whether/how efficiently the goal is
  reached.
- **Difficulty control**: difficulty-calibrated via extensive human testing (so
  difficulty is empirically pinned to human solve rates, not a generative knob).
- **Memorization prevention**: environments are novel and hand-authored per release
  (not procedurally generated at scale, based on what's available) — anti-memorization
  relies on genuine novelty/secrecy of held-out environments, not a parametric generator.
  **[inferred — could not confirm generation method]**
- **Human baseline**: humans solve 100% of environments.
- **Layers?** Not described as nested-validity regimes; more about hidden goals and
  dynamics under exploration, single-environment scope per task.
- **Scores/saturation**: frontier AI systems score **below 1%** as of March 2026 — this
  is the single most unsaturated benchmark in the set, essentially the opposite failure
  mode from NewtonBench-style gradual degradation.

### "Can LLM Agents Infer World Models? Evidence from Agentic Automata Learning" — arXiv 2606.16576
Menaged, Lior, Ravfogel, Aharoni, Stanovsky. https://arxiv.org/abs/2606.16576
- **World**: a hidden deterministic finite automaton (DFA); this is the cleanest,
  most abstract "hidden structure" setup in the set — no physics dressing at all.
- **Agent actions**: membership queries ("does string X belong to the language?") and
  equivalence queries ("is this the target DFA?") — classic Angluin-style active
  automata learning, now posed to an LLM tool-calling agent instead of a symbolic
  learner.
- **Submitted / graded**: an explicit automaton, compared for equivalence to ground
  truth; strong non-LLM baselines exist (classical automata-learning algorithms like
  L*), which is a genuinely rigorous grading reference class other papers here lack.
- **Difficulty control**: DFA size (states/alphabet) — clean, scalable, continuous knob.
- **Memorization prevention**: procedurally generated random DFAs — nothing to recall
  from pretraining.
- **Human baseline**: not reported.
- **Layers?** No nested regimes — a DFA is a single flat rule, though larger DFAs can be
  seen as encoding more "depth" of state-dependent behavior (a naive agent might
  overfit to a small subset of reachable states, analogous to a shallow theory that
  works in the observed regime and fails once new states are reached — **this is the
  closest structural analogy to a "reachable anomaly" in the set, though the paper
  frames it as scale, not depth** — **[my inference, not the paper's framing]**).
- **Scores**: performance "drops sharply" as DFA size increases; reasoning models beat
  non-reasoning models but still show recurring failures in query planning, evidence
  integration, and hypothesis construction — i.e. the failure is in the *experiment
  design* loop, not just pattern-fitting.

### CellARC — arXiv 2511.07908
https://arxiv.org/abs/2511.07908, https://cellarc.mireklzicar.com/
- **World**: multicolor 1D cellular automata; each episode gives 5 support pairs +1
  query, serialized in 256 tokens.
- **Agent actions**: none beyond in-context few-shot inference — this is not an
  interactive/interventional benchmark, it's closer to ARC-style few-shot induction.
  **No experimentation loop.**
- **Difficulty control**: explicit, generative knobs — alphabet size k, neighborhood
  radius r, rule family, **Langton's lambda** (a classic CA complexity/criticality
  parameter), query coverage, cell entropy. This is the most explicit and well-thought-
  out "generator with a depth/complexity knob" in the whole set, directly relevant to
  our "generator needs a depth knob" design requirement — though the knob controls CA
  complexity/chaoticity, not nested regimes of validity.
- **Memorization prevention**: unlimited procedural sampling, interpolation vs.
  extrapolation test splits.
- **Human baseline**: not reported (compares symbolic/RNN/CNN/transformer/recursive/LLM
  baselines).
- **Layers?** No regime-nesting — single CA rule per episode, one flat ground truth.
- **Scores**: a 10M-parameter plain transformer beats recent recursive architectures
  (TRM, HRM): 58.0%/32.4% per-token accuracy on interpolation/extrapolation. Notably
  this is a benchmark where a *tiny* trained model beats fancier architectures, a useful
  cautionary data point about benchmark design (capacity/inductive bias can matter more
  than architecture novelty at this scale).

### 2507.12821 — "Assessing Adaptive World Models in Machines with Novel Games"
Ying, Collins, Sharma, Colas, Zhao, Weller, Tavares, Isola, Gershman, Andreas,
Griffiths, Chollet, Allen, Tenenbaum. https://arxiv.org/abs/2507.12821
- This is the paper CLAUDE.md/memory says the project is already anchored on. It is a
  **position/framework paper**, not itself a shipped benchmark with scores — it argues
  (drawing on cognitive-science literature on human rapid learning/adaptation) for a new
  evaluation paradigm using **novel games** to test adaptive world-model formation,
  explicitly because existing static benchmarks don't test *in-context* model building
  and revision. Its authors include Chollet (ARC-AGI) and Tenenbaum/Gershman
  (computational cognitive science) — i.e. it is the conceptual ancestor of both
  ARC-AGI-3 and AutumnBench above, and is likely part of why our project already treats
  it as the anchor. **[I did not find a released dataset/benchmark artifact from this
  paper specifically, distinct from ARC-AGI-3 and AutumnBench, which are its
  apparent operationalizations — flag as needing a closer read.]**

### CausalGame — arXiv 2607.04293
https://arxiv.org/abs/2607.04293, ICML 2026.
- **World**: 14 game scenarios engineered to contain **selection bias, measurement
  error, and hidden confounders** — deliberately not clean causal graphs.
- **Agent actions**: design experimental protocols, collect data, submit a causal
  explanation report.
- **Submitted / graded**: a "solution" scored for "survival" against an analytical
  optimum (78-85%), plus a causal-reasoning rubric.
- **Difficulty control**: which bias/confound types are injected per scenario.
- **Memorization prevention**: **[unverified]** — not confirmed whether scenarios are
  parametrically regenerated or fixed/curated (14 scenarios suggests curated, not
  generated at scale — a possible weakness).
- **Human baseline**: not found.
- **Layers?** The confounders/measurement-error framing is adjacent to our "shallow
  theory fails" idea (a naive causal read is wrong until you account for the hidden
  confounder) but it's presented as **bias to detect and correct for**, not as **a
  deeper regime reachable through further intervention** — closer to robust statistics
  than to "Newton until you go fast."
- **Scores**: best of 30 LLM agents reaches 68.0% vs 78-85% analytical optimum; only
  5-7% of sessions get credit on the causal-reasoning rubric specifically — i.e. models
  can sometimes get the right answer without demonstrating real causal reasoning,
  which the authors treat as a genuine benchmark validity concern.

### DiscoverPhysics — arXiv 2605.26087 [fetched abstract]
Wiemann, Smith, Melchior, Mishra-Sharma, Wilson, Izmailov, Cuesta-Lázaro.
https://arxiv.org/abs/2605.26087
- **World**: 22 N-body-simulated worlds with physics **deliberately deviating from our
  universe**: screened/fractional-power gravity, multi-species couplings, hidden
  dark-matter-like particles, non-coordinate-free dynamics, time-varying interactions.
  This is the entry in the set with the richest "alternate physics" flavor.
- **Agent actions**: multiple rounds of proposed experiments, observing raw trajectory
  data from the simulator.
- **Submitted / graded**: (1) a natural-language explanation, scored by an LLM judge
  against an expert-written rubric for conceptual understanding, and (2) a Python
  implementation of the inferred law, scored by trajectory MSE on held-out particles.
  This two-channel grading (explanation quality + executable/predictive accuracy) is a
  useful pattern — it catches models that get a plausible-sounding story without a
  working simulator, and vice versa.
- **Difficulty control**: **[unverified]** not found explicitly, likely via which of the
  22 non-standard physics variants is used and how many interacting species/particles.
- **Memorization prevention**: the physics is intentionally *wrong* relative to reality
  (dark-matter-like hidden particles, screened gravity, etc.), so textbook recall
  actively hurts rather than helps — similar strategy to NewtonBench's counterfactual
  shifts, applied at the level of whole dynamical systems rather than single laws.
- **Human baseline**: not found.
- **Layers?** **Closest single-flat-law-vs-depth analog in the set is arguably here**:
  "hidden dark-matter-like particles" and "screened gravity" are exactly the *kind* of
  physics where a naive theory (ordinary gravity) fits until you reach a regime
  (galactic scales / hidden mass) where it breaks and a deeper theory (extra unseen
  mass, screening mechanism) is needed — this is structurally very close to what we
  want. But as far as I could verify, **each of the 22 worlds still has one single
  fixed non-standard law active throughout, not a nested "law A near / law B far"
  transition inside one world** — so the *ingredients* for regime-nesting are all
  present in this design lineage but the paper doesn't appear to assemble them into an
  intra-world regime transition. **[This is my inference; needs a full-text read to
  confirm the sim doesn't already do this.]**
- **Scores**: strongest agents pass only ~half the worlds and "consistently fail on
  those where latent structure must be uncovered" (e.g., an unobserved extra particle)
  — i.e. failure concentrates exactly on the hidden-structure-inference worlds, which
  is a strong signal that hidden/deeper structure is the hard part, supporting our
  design bet.

### LLM-AutoSciLab / ActiveSciBench — arXiv 2605.24043
Kabra, Abhyankar, Desai, Iyer, Reddy (Virginia Tech / Sandia). https://arxiv.org/abs/2605.24043
- **World**: enzyme-kinetics (57 tasks) and gene-regulatory-network (45 tasks) discovery
  problems; a closed loop of hypothesis generation → hypothesis-conditioned experiment
  selection → mechanism refinement, explicitly against "reduce discovery to supervised
  learning over a fixed dataset" which they diagnose as the field's core failure mode
  (multiple mechanisms fit locally but don't generalize without active data acquisition).
- **Agent actions**: iteratively propose hypotheses, choose next experiment to run.
- **Submitted / graded**: symbolic accuracy against ground-truth mechanism / exact
  graph recovery (GRN case).
- **Reported scores**: 67.6% symbolic accuracy on NewtonBench, 35.1% on
  ActiveSciBench-Chem, 31.1% exact graph recovery on ActiveSciBench-GRN; their
  active/hypothesis-guided method is 2-5x more sample-efficient than passive baselines.
- **Layers?** No nested regimes — single fixed mechanism per task; the "multiple
  plausible mechanisms fit locally" problem the authors name is about underdetermination
  from sparse data, not depth-of-theory, but it's a closely related failure mode (a
  locally-adequate but globally-wrong model) worth citing for our motivation section.

### AI-Newton — arXiv 2504.01538
Fang et al. https://arxiv.org/abs/2504.01538
- **World**: not a benchmark environment per se — a **discovery system** (algorithm),
  evaluated by its ability to rediscover known classical mechanics (Newton's second law,
  gravitation, conservation laws) from experimental data, with **no prior physical
  concepts** (mass, energy, etc. are themselves discovered, not given).
- **Mechanism**: three-layer theory base (symbols → concepts → laws), built via
  plausible reasoning over a physics DSL.
- **Relevance to us**: this is evidence that *concept layering* (raw symbols → derived
  concepts → laws) is a natural and productive structure for a discovery system to
  build internally, which is a different sense of "layers" than our nested-regimes idea
  (this is layers-in-the-discovered-theory's dependency graph, not layers-in-when-the-
  theory-is-valid) — worth distinguishing explicitly since the word "layers" is
  overloaded across this literature.
- **No falsification/regime-breaking test**: it's tested on rediscovering *true*
  classical mechanics, not on a world where classical mechanics later breaks.

### AI Feynman — arXiv 1905.11481 (Udrescu & Tegmark, Science Advances 2020)
https://arxiv.org/abs/1905.11481
- **World**: 100 "Feynman equations" (real textbook physics formulas) + a bonus set of
  harder ones, given as input-output tuples, no interaction/experimentation — pure
  symbolic regression from a fixed dataset.
- **Method insight most relevant to us**: reframes symbolic regression as **recursive
  structure discovery** (dimensional analysis, then detecting symmetry/separability to
  recursively split a hard high-dimensional problem into simpler sub-problems) rather
  than one flat global search. This recursive-decomposition idea (find where a simpler
  sub-theory applies, then compose) is conceptually adjacent to regime-nesting, though
  applied to *equation structure*, not to *validity regimes in the world*.
- **Scores**: solved 100% of the 100 core equations and 90% of the bonus set (vs. 68%/15%
  for prior SOTA "Eureqa"), under a 2-hour CPU budget — an old benchmark that is fully
  saturated by design (fixed, static, no adversarial regeneration), illustrating exactly
  the memorization/staleness risk our generator needs to avoid.
- **Layers?** No — flat formulas, no world, no regime transitions.

### Alchemy (DeepMind) — arXiv 2102.02926
Wang et al., NeurIPS 2021 D&B. https://arxiv.org/abs/2102.02926
- **World**: a 3D first-person Unity game where stones/potions have a **latent causal
  structure resampled every episode** (a hidden chemistry graph mapping potions to
  stone-state transformations); agent must infer the hidden graph through
  intervention (dunking stones in potions) then act on it for reward.
- **Agent actions**: full embodied intervention within the episode; explicit
  experimentation/hypothesis-testing/action-sequencing loop, meta-RL setting (learn to
  learn across episodes with resampled structure).
- **Submitted / graded**: reward accumulated via correct exploitation of the inferred
  latent structure within the episode — implicit, not an explicit "submit a theory"
  step (weaker than our design in that sense, since there's no exact program grading).
- **Difficulty/memorization**: structure is **procedurally resampled every episode**,
  which is the cleanest "can't memorize, must actually infer" mechanism in the whole
  set, and matches our "procedurally generated" requirement almost exactly.
- **Layers?** No nested regimes-of-validity — one latent causal graph per episode,
  fully static within the episode. But structurally the closest ancestor to "own the
  generator, resample hidden structure procedurally, own ground truth" of anything
  surveyed, which is presumably why the project (per memory) is already anchored partly
  on this lineage of ideas.
- **Age/limits**: 2021, symbolic + full 3D versions both open-sourced; predates the
  LLM-agent wave, so no LLM scores exist for it as tested in this set.

### IVRE — arXiv 2206.09203
Xu, Jiang, Liang, Zhang, Zhu, NeurIPS 2023 D&B. https://arxiv.org/abs/2206.09203
- **World**: Blicket-detector scenarios (classic developmental-psych causal-learning
  paradigm) — objects may or may not be "blickets" (activate a machine); ambiguous
  action-effect pairs force active intervention to disambiguate.
- **Agent actions**: propose experiments (which objects to place on the machine) to
  actively resolve hypothesis ambiguity, rather than just observe.
- **Layers?** No — single hidden binary-labeling function per scenario (which objects
  are blickets), no regime transitions. But it's a clean minimal instance of "ambiguous
  under passive observation, resolvable only by intervention," which is the same
  design principle behind the "N_smart vs N_random" question in the project's own
  Active-induction-target memory note — worth citing there.

### InductionBench — arXiv 2502.15823
ACL 2025. https://arxiv.org/abs/2502.15823, https://github.com/Wenyueh/inductive_reasoning_benchmark
- **World**: string-to-string transformation functions drawn from the **subregular
  hierarchy** (a formal-language-theory complexity ladder with known
  polynomial-time/data learnability guarantees at each level) — genuinely
  complexity-graded, not just "harder-feeling."
- **Agent actions**: propose test strings, observe outputs (active querying), or
  passive fitting — includes a **Wason 2-4-6-style task** (infer x<y<z from proposed
  triples) explicitly testing confirmation-bias-prone hypothesis testing.
- **Submitted / graded**: the inferred transformation function, checked for
  correctness and for **minimality/non-redundancy** of the hypothesis (not just
  "fits the data" but "is the simplest consistent rule") — a sharper grading criterion
  than most entries here.
- **Difficulty control**: position in the subregular hierarchy — theoretically
  principled, not ad hoc.
- **Layers?** No nested regimes — single flat transformation function per task, but the
  hierarchy itself is a nice model for how *we* might define a "depth knob" with formal
  learnability guarantees at each depth, rather than an ad hoc noise/complexity dial.
- **Scores**: even frontier models "fail in the simplest complexity class" (per title) —
  strong unsaturated result, and a cautionary note that even very simple flat rules
  already break current LLMs, which bears on how much "depth" we can expect discovery
  agents to handle at all right now.

### FalsifyBench — arXiv 2606.04751
https://arxiv.org/pdf/2606.04751
- **World**: rule-discovery games grounded in semantic taxonomies, explicitly built
  around the ability to **generate a hypothesis and then actively try to falsify it**
  (rather than only seek confirming evidence) — i.e. it operationalizes
  Popperian falsification as the graded skill, closest in spirit of anything found to
  "theory revision as the core loop" named in our brief.
- Evaluated on 12 LLM families/scales. **[Found via search only; not fetched in full —
  flag for a follow-up close read since it's thematically the closest match to the
  falsification angle of the brief.]**
- **Layers?** Not confirmed from snippet whether tasks nest regimes or are flat rules
  needing a single falsification step; likely closer to Wason-2-4-6-style flat rule
  discovery. **[unverified]**

---

## Comparison table

| Benchmark | World type | Agent can intervene? | What's submitted | Grading | Difficulty knob | Anti-memorization | Human baseline | Nested regimes (layers)? | Frontier score / saturation |
|---|---|---|---|---|---|---|---|---|---|
| NewtonBench (2510.07172) | simulated physics, altered laws | yes | inferred law | match vs. altered ground truth | # variables, noise | counterfactual law shifts | not found | No — flat altered law | fragile, degrades fast w/ complexity |
| DiscoveryWorld (2406.06769) | text/grid sci-discovery sim | yes | action/decision | oracle answer key | normal/challenge tiers | task variation (weak) | yes, ~100% human vs. ~20% best agent | No | ~80% agent failure, far from saturated |
| PhysGym (2507.15550) | interactive physics sim | yes | hypothesis | not confirmed | prior-knowledge level + complexity | prior-knowledge occlusion | not found | No | not confirmed |
| BoxingGym (2501.01540) | probabilistic generative models (psych/eco) | yes | design choices + explanation | EIG (design), predictive use of explanation | not explicit | live interrogation, not lookup | not found | No | GPT-4o-class struggles on both axes |
| SciGym (2507.02083) | real SBML biology networks | yes (perturb + code) | reconstructed model | not confirmed | network size/complexity | unresolved — real models could leak | not found | No | only 6 LLMs on small subset tested |
| AutumnBench/WorldTest (2510.19788) | grid worlds, train/test env split | yes (phase 1 only) | answers to env-level queries | vs. ground truth | not explicit | different test env than train env | yes, 517 humans vs. 3-5 models, humans win | No (transfer, not depth) | uneven — scaling helps some envs, not others |
| ARC-AGI-3 (2603.24621) | abstract turn-based grid worlds, hidden goals | yes | implicit goal completion | task success | human-calibrated | novel hand-authored envs | 100% human | No | <1% frontier AI — most unsaturated here |
| Agentic Automata Learning (2606.16576) | hidden DFA | yes (membership/equivalence queries) | equivalence claim / automaton | exact equivalence vs. classical baselines | DFA size | random generation | not found | No (flat, but scale ~ reachability of new states) | drops sharply with DFA size |
| CellARC (2511.07908) | 1D cellular automata | no (few-shot only) | predicted output cells | exact match | k, r, rule family, Langton's λ, entropy | procedural + interp/extrap splits | not found | No | tiny transformer beats fancier recursive models |
| CausalGame (2607.04293) | games w/ bias/confounders | yes | causal explanation report | survival vs. analytical optimum + rubric | which biases injected | unresolved, likely curated (14 scenarios) | not found | Adjacent (bias to correct, not regime to escape) | best 68% vs 78-85% optimum; only 5-7% pass rubric |
| DiscoverPhysics (2605.26087) | N-body sim, alternate physics | yes | NL explanation + Python law | LLM-judged rubric + trajectory MSE | not confirmed | non-standard physics (unlearnable from pretraining) | not found | Ingredients present (hidden dark matter, screened gravity) but not assembled as intra-world regime transition | ~half worlds passed; fails concentrate on hidden-structure worlds |
| LLM-AutoSciLab/ActiveSciBench (2605.24043) | enzyme kinetics, GRNs | yes | symbolic mechanism / graph | accuracy vs ground truth | task domain size | real bio tasks, not clear | not found | No (underdetermination, not depth) | 31-68% depending on task |
| AI-Newton (2504.01538) | classical mechanics rediscovery | yes (its own experiments) | symbols→concepts→laws | rediscovers known laws | n/a (proof of concept) | n/a | not found | Concept-dependency layers, not validity-regime layers | rediscovers Newton's laws, conservation laws |
| AI Feynman (1905.11481) | 100 static physics formulas | no | symbolic formula | exact match | n/a | none — fully static, saturated | not found | No | 100%/90% — fully saturated, stale by design |
| Alchemy (2102.02926) | 3D game, resampled latent chemistry | yes, embodied | in-episode reward (no explicit theory submission) | task reward | n/a | resampled every episode | not found | No, but structure/generator lineage is closest ancestor of our approach | pre-LLM, no comparable scores |
| IVRE (2206.09203) | Blicket-detector scenes | yes | hypothesis about object roles | vs. ground truth labeling | not explicit | new scene per trial | not found | No | not found in snippets |
| InductionBench (2502.15823) | subregular string transformations | yes (active querying) | minimal transformation function | correctness + minimality | position in subregular hierarchy | formally graded difficulty | not found | No, but hierarchy = principled depth-knob model | fails even simplest complexity class |
| FalsifyBench (2606.04751) | taxonomy-grounded rule games | yes | falsification attempts / hypothesis | rubric | not confirmed | not confirmed | not found | unconfirmed | not confirmed |

---

## Key question: has anyone built discovery worlds with nested regimes of validity and theory revision as the core loop?

**No — not as far as this search found.** Every benchmark surveyed has, per task or per
episode, **one single fixed ground-truth rule/law/graph/automaton that is true
everywhere the agent can probe it.** "Revision" in this literature means:
- narrowing uncertainty about parameters of one fixed model (BoxingGym),
- resolving ambiguity among competing hypotheses that are locally indistinguishable
  from sparse data (LLM-AutoSciLab, IVRE, Wason-style tasks),
- correcting for a fixed confound/bias baked into one causal graph (CausalGame),
- or discovering ever-larger/harder instances of one flat rule class (InductionBench,
  agentic automata learning, CellARC).

None of these is a world where a **theory that is correct and sufficient in the observed
regime becomes actively wrong once the agent reaches a further regime**, forcing a
genuine *replacement* of the theory rather than a *refinement* of its parameters. The
closest approach is **DiscoverPhysics (2605.26087)**, whose ingredient list — screened
gravity, hidden dark-matter-like particles, non-coordinate-free physics — is exactly the
kind of real-physics phenomenon that *does* produce regime breaks (Newtonian gravity is
"screened" / breaks down at certain scales in real screened-gravity theories; hidden
mass is undetectable until you look at large-scale dynamics). But based on what I could
verify, each of DiscoverPhysics's 22 worlds runs one non-standard law throughout, rather
than nesting "law A applies for |v| ≪ c, law B takes over for |v| ≈ c" inside a single
world. This is an inference from the abstract, not a confirmed absence — **it needs a
full-text/code check before we claim novelty over it.**

**AutumnBench/WorldTest** and **ARC-AGI-3** get partway there on a different axis: they
separate a *training/interaction* environment from a *test* environment that is
"different but related," which forces genuine generalization rather than memorized
answers — but this is generalization across environments, not depth-of-theory within
one environment.

**The gap**: no surveyed benchmark makes "a shallow theory fits until a reachable
anomaly breaks it, and the agent must revise to a deeper theory" the *generative,
built-in, unavoidable structure of the world itself* — as opposed to a scripted "gotcha"
task. This matches the brief's instinct: the properties need to emerge from the world
construction, and nobody in this list appears to have built a generator with that
property as a first-class knob.

## Design mistakes / limitations the papers admit to

- **NewtonBench**: giving agents a code interpreter can *hurt* the strongest models —
  they prematurely stop exploring and settle for a locally-fitting but wrong law. Lesson
  for us: tooling access changes exploration behavior in ways that can mask or create
  failure to reach deeper regimes; worth testing with and without scaffolding.
- **BoxingGym**: adding explicit statistical modeling support did not reliably help
  agents — same shape of lesson, scaffolding is not free.
- **CausalGame**: authors flag that models can pass the top-level "survival" metric
  (68% vs 78-85% optimum) while only 5-7% of sessions get credit on the actual
  causal-reasoning rubric — i.e. **outcome-based grading alone can be gamed/lucky-guessed
  without real understanding**, which is exactly why DiscoverPhysics's two-channel
  grading (explanation rubric + executable trajectory match) and BoxingGym's
  "explanation must let another agent predict" test are better patterns than raw task
  success. **We should grade the submitted program's behavior AND require it to
  generalize to held-out/deeper regimes, not just match on the observed regime.**
- **SciGym**: real curated biological models risk pretraining leakage/memorization —
  the paper does not appear to fully resolve this (based on what I could access);
  general lesson reinforcing why our brief insists on **owned, procedurally generated**
  simulators rather than borrowed real-world datasets.
- **AI Feynman**: is a cautionary tale about staleness — a fixed, static, non-adversarial
  benchmark from 2019 that was fully saturated (100%/90%) essentially immediately once a
  well-designed method (its own) was applied, and remains reused since with no
  regeneration mechanism. Reinforces the brief's "cheap, procedurally generated" and
  presumably "resistant to a single trick solving it forever" requirements.
- **CellARC**: a tiny (10M param) plain transformer beat fancier recursive architectures
  (TRM, HRM) — a reminder that a new benchmark can accidentally reward brute-force
  pattern-matching capacity over the "real" targeted skill (rule induction), if the
  generator's task distribution is too learnable by memorizing surface statistics. We
  should stress-test our own generator against small non-agentic baselines for this
  failure mode.
- **AutumnBench**: explicitly built its train/test split methodology *because* prior
  world-model benchmarks let agents overfit to properties of a single environment
  instance rather than learning a genuinely predictive model — direct precedent for
  why we should validate any submitted "theory" against a held-out regime, not just
  replay of the training regime.

## 5 concrete world-design ideas implied by this literature

1. **Borrow the "screened/hidden-mass gravity" trick from DiscoverPhysics (2605.26087),
   but nest it explicitly.** Build a world where a simple, easily-discoverable rule
   (e.g., a 2-body inverse-square-like law) holds exactly under normal
   observation-reachable conditions, and a second, only-reachable-through-intervention
   regime (e.g., extreme separation, extreme mass ratio, or an added hidden body) makes
   the simple rule measurably wrong, requiring an explicit "extra hidden term" to fix —
   i.e., do intentionally, inside one world, what DiscoverPhysics's ingredient list
   makes possible but (as far as verified) doesn't assemble across regimes within a
   single world instance. Source: arXiv 2605.26087.
2. **Use Alchemy's "resample the latent structure every episode, own the generator"
   pattern (2102.02926) as the procedural-generation backbone**, but add a depth
   parameter that controls how many strata of hidden causal structure exist (a
   "meta-graph of graphs"): shallow strata are reachable by cheap experiments, deeper
   strata require specific, more expensive/rare interventions to expose — giving us the
   "depth knob" the brief asks for, grounded in a benchmark design already proven
   workable for meta-RL. Source: arXiv 2102.02926.
3. **Take InductionBench's subregular-hierarchy idea (2502.15823)** — a formally graded
   ladder of rule classes with known learnability guarantees — and use an analogous
   formal ladder (e.g., increasing order of an implicit differential equation, or
   increasing degree of a hidden polynomial correction term) as the actual "depth" axis
   of our generator, so difficulty isn't just vibes but has a provable structure, and
   we can report where on the ladder current models plateau. Source: arXiv 2502.15823.
4. **Adopt AutumnBench/WorldTest's train/interaction vs. test/query separation
   (2510.19788)** as our grading protocol: let the agent freely intervene in the
   "normal regime" of a world, then test its submitted program's predictions in a
   *different, deeper regime it was never directly shown* — this operationalizes "fit,
   fail, investigate, revise" as a scored protocol rather than trusting self-report, and
   gives us a clean way to detect agents that memorized surface behavior versus ones
   that found the deeper generative rule. Source: arXiv 2510.19788.
5. **Use DiscoverPhysics's and CausalGame's two-channel/rubric grading pattern
   (2605.26087, 2607.04293)** — grade both (a) the submitted program's exact behavioral
   match against our simulator on held-out/deeper-regime inputs (hard, exact, since we
   own the simulator per the brief) and (b) whether the agent's own account of *why* its
   theory needed revision correctly identifies the anomaly and the deeper mechanism —
   to avoid CausalGame's admitted problem of agents "surviving" without demonstrating
   real understanding. Source: arXiv 2605.26087, arXiv 2607.04293.

## Flagged for follow-up (not fully verified this pass)

- PhysGym human baseline/scores — search snippets didn't surface numbers; worth a
  direct read of https://arxiv.org/pdf/2507.15550.
- SciGym's exact grading metric and any anti-leakage protocol for real BioModels —
  https://arxiv.org/html/2507.02083.
- FalsifyBench (2606.04751) — thematically the closest match to "falsification as core
  loop" in the brief; only searched, not fetched — https://arxiv.org/pdf/2606.04751.
- DiscoverPhysics full text — need to confirm whether any of the 22 worlds actually
  does nest two regimes within a single world (my read of the abstract suggests one
  fixed law per world, but this is inference, not confirmed) —
  https://arxiv.org/html/2605.26087v1.
- 2507.12821's own operational benchmark artifact, if one exists beyond ARC-AGI-3/
  AutumnBench as its apparent downstream instantiations — https://arxiv.org/abs/2507.12821.
