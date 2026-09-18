# Discrete substrates with layered laws: lattice gases, block CA, particle CA, chemistries, criticality

Angle: which discrete, deterministic, cheap substrates naturally have (a) a simple emergent
law that holds in a common regime, (b) a reachable regime where it breaks, and (c) conserved
quantities / emergent objects an experimenter could discover. Compared against Conway-Life
grids as baseline.

## 1. Lattice gas automata (HPP, FHP) — the cleanest literature example of a layered world

- **Lattice gas automaton**, Wikipedia overview, https://en.wikipedia.org/wiki/Lattice_gas_automaton
  — Says: LGA are boolean-occupation CA on a lattice with particles moving and colliding under
  local, deterministic (or randomized-tiebreak) rules; from local mass/momentum-conserving
  collision rules the macroscopic Navier-Stokes equations can be derived by a Chapman-Enskog-style
  expansion. Why it matters: this is a documented case of a microscopic discrete rule provably
  producing a higher-level continuum law.
- **Lattice-Gas Automata for the Navier-Stokes Equation**, Frisch, Hasslacher, Pomeau, Phys. Rev.
  Lett. 56, 1505 (1986), https://link.aps.org/pdf/10.1103/PhysRevLett.56.1505
  — Primary paper. Says: the HPP model (square lattice, 4 velocity directions) is the first fully
  deterministic LGA but its collision rules don't have enough rotational symmetry — the derived
  stress tensor is anisotropic, so it visibly fails to obey the isotropic Navier-Stokes equations
  except in special-case flows. The FHP model (triangular lattice, 6 directions) has enough
  discrete symmetry that the anisotropic terms cancel and the incompressible Navier-Stokes
  equations emerge rigorously in the long-wavelength, low-Mach-number limit.
- **Lattice Gases and Cellular Automata**, review, https://arxiv.org/pdf/comp-gas/9905001
  — Confirms the same story and adds: LGA suffer statistical noise from boolean occupation
  variables, motivating the later Lattice Boltzmann method (real-valued distribution functions
  instead of bits) as a smoother, less noisy descendant.
- **Emergent dynamic structures and statistical law in spherical lattice gas automata**,
  https://arxiv.org/pdf/1712.09450 — Says LGA on curved/spherical lattices still generate
  statistical fluid-like laws, i.e. the emergence is robust to the underlying lattice geometry,
  not a fluke of the flat triangular lattice.

**Why this is the best-documented "layers" substrate we found**: The literature explicitly
frames this as a *hierarchy of validity regimes*, verified quantitatively:
1. Microscopic layer: exact reversible/deterministic bit-level dynamics (the true law, always
   true, but useless for prediction because of combinatorial state size).
2. Mesoscopic layer: a derived law (Navier-Stokes) that holds ONLY when the CA has enough
   discrete symmetry (triangular, not square lattice) — this is a "depth knob" already built in:
   swap square→triangular lattice and you get "Newton" (HPP, breaks/anisotropic) vs. "General
   Relativity" (FHP, correct in its regime).
3. Regime of breakdown: high Mach number / high Reynolds number / short wavelength — the
   continuum law breaks and only the microscopic rule remains correct, exactly the "Newton works
   until you go fast" structure requested in the brief.
4. Conserved quantities: particle number and momentum per collision are exactly conserved by
   construction (that's what licenses the continuum derivation) — an obvious target for an agent
   to "discover" by poking a region and checking invariants across a collision.

**Inference (mine, not sourced)**: LGA is almost a direct template for the benchmark's generator:
pick a lattice symmetry parameter (few discrete choices) as a "depth knob" — low-symmetry lattice
= shallow, visibly-broken effective theory in most regimes; high-symmetry lattice = effective
theory holding over a wider domain, breaking only at extreme parameters (high density/speed).
This gives cheap, deterministic worlds with a literal derivable macroscopic theory, a documented
failure mode, and countable conserved quantities.

## 2. Reversible / block cellular automata (Margolus neighbourhood, Critters, Billiard Ball Model)

- **Norman Margolus**, Wikipedia, https://en.wikipedia.org/wiki/Norman_Margolus — Margolus
  invented the block CA / Margolus-neighbourhood update (partition the grid into 2x2 blocks,
  alternate the partition phase every step) specifically to build *reversible* CA — a substrate
  where microscopic information (and hence a literal "conserved phase-space volume") is never
  destroyed, mirroring physical reversibility.
- **Critters (cellular automaton)**, Wikipedia, https://en.wikipedia.org/wiki/Critters_(cellular_automaton)
  — Says: Critters (Toffoli & Margolus, 1987) is a reversible block CA using the Margolus
  neighbourhood with Life-like glider/still-life dynamics but, unlike Conway's Life, is provably
  information-conserving (it's a bijection on global states) — you can run it backwards exactly.
- **Computing Inside the Billiard Ball Model**, Springer chapter,
  https://link.springer.com/chapter/10.1007/978-1-4471-0129-1_6 — Margolus's billiard-ball-model
  CA emulates hard-sphere billiard collisions (momentum/energy-conserving elastic collisions) on
  a block-CA substrate and is Turing-universal via reversible logic gates (Fredkin gates) built
  from ball trajectories and mirrors.

**Layers reading**: at the microscopic level the update is a fixed, simple local swap-rule
applied uniformly; at a coarser level, in low-density regimes balls behave like a dilute gas
obeying straight-line-motion-plus-elastic-collision "billiard mechanics" (a simple effective
law), but in dense/crowded regimes multi-body pile-ups and blocked trajectories break the
naive single-particle picture — the failure mode is *reachable by turning up a density knob*.
Exact reversibility gives a hard invariant (bijectivity / phase space volume, plus explicit ball
count and momentum in the BBM) that an agent could try to falsify and never succeed, functioning
as a "law that never breaks" contrasted against ones that do.

**Comparison to Conway-Life-style grids**: ordinary Life is irreversible (many-to-one map: gardens
of Eden, convergent still lifes), so information/energy-like quantities are NOT conserved — good
for "interesting patterns" but bad as a substrate for teaching an agent about conservation laws,
since there is no ground-truth invariant to recover. Margolus/Critters-style reversible block CA
keep the same glider/emergent-object aesthetic as Life while adding an actual provable invariant
(the global state map is a bijection), which is exactly the kind of "conserved quantity to
discover" the brief wants. This is a concrete argument for preferring a reversible block-CA
substrate over vanilla Life when conservation laws are a required discoverable property.

## 3. 1-D elementary CA: gliders as literal particles with a collision calculus (Rule 54, Rule 110)

- **A Language for Particle Interactions in Rule 54 and Other Cellular Automata**, Crutchfield et
  al., https://www.researchgate.net/publication/318916115_A_Language_for_Particle_Interactions_in_Rule_54_and_Other_Cellular_Automata
  and the underlying **ECA54 domain/particle analysis**, https://csc.ucdavis.edu/~cmg/papers/ECA54.pdf
  — Says: Rule 54's spacetime diagram decomposes into a homogeneous "domain" (background regular
  pattern, effectively the vacuum/ground state) plus localized "particles" (gliders) that move at
  fixed velocities through the domain and have a small, enumerable catalog of collision products.
  This is explicitly a *computational mechanics* result: filtering out the domain reveals discrete
  particle-like objects whose interactions can be written as a small grammar/calculus, analogous
  to writing down chemistry from an underlying field theory.
- **Upper Bound on the Products of Particle Interactions in Cellular Automata**, Hordijk, Shalizi,
  Crutchfield, Physica D 2001, https://arxiv.org/pdf/nlin/0008038 — Says: for a broad class of CA
  the number of possible outgoing particle species after a collision is provably bounded, i.e.
  there is a derivable, checkable "conservation-like" law constraining what collision outcomes are
  reachable — closely analogous to inferring selection rules from particle-physics data.
- **Mechanisms of Emergent Computation in Cellular Automata**, Hordijk, Mitchell, Crutchfield
  (PPSN V, 1998), referenced via https://www.researchgate.net/publication/2639886 — Rule 110's
  gliders and collisions are the mechanism behind its Turing-universality (Cook's proof uses
  glider collisions as logic gates); this ties the "particle calculus" of 1-D CA directly to
  computational power, not just decoration.

**Layers reading**: the domain (background pattern) is the "simple effective theory" — most of the
lattice, most of the time, is well-described by "nothing happens, uniform periodic background."
The rare, reachable regime where the simple theory fails is exactly where a particle passes
through, or two particles collide — locally violating the "boring domain" prediction and requiring
the deeper particle-collision rulebook to explain what happens next. This is an unusually literal,
minimal instance of "shallow theory holds almost everywhere, breaks in a small but reachable
region, and a catalog of deeper rules explain the break," and it is *cheap*: 1-D, few states,
trivial to generate variants of (different ECA rule numbers) as a difficulty/depth knob — e.g. an
agent must discover 2-3 domains and their gliders rather than one.

## 4. Continuous-state CA: Lenia and Flow-Lenia — mass conservation as a discoverable law

- **Flow-Lenia: Emergent Evolutionary Dynamics in Mass Conservative Continuous Cellular
  Automata**, Plantec, Hamon, Etcheverry, Chan, Oudeyer, Moulin-Frier, Artificial Life 2025 (arXiv
  2506.08569, and earlier arXiv 2212.07906), https://arxiv.org/abs/2506.08569 /
  https://arxiv.org/pdf/2212.07906 — Says: base Lenia produces localized, organism-like patterns
  ("creatures": self-propelling, sometimes self-replicating), but standard Lenia does not conserve
  mass, which limits multi-creature ecology (patterns can grow/shrink/vanish arbitrarily). Flow-Lenia
  reformulates the update as a mass-conserving flow field (advection-like transport of "matter")
  so total mass is an exact global invariant, enabling stable multi-species ecosystems and even
  embedding rule-parameters in the field itself (open-ended, spatially heterogeneous physics).
- Relation to substrate depth: because parameters can be localized in space, different regions of
  the same world can literally run under different local "physics" — a built-in mechanism for
  planting a rare region with a different effective rule, i.e. a literal depth/anomaly knob rather
  than an emergent one.

**Layers reading**: the discoverable "simple law" is mass conservation and characteristic organism
shapes/velocities in the common regime (bulk of the field, well-separated creatures); the
"breaking regime" is creature collision/merging events and boundary regions with different local
parameters, where the simple single-creature kinematics laws fail and the underlying convolution
+ flow-field rule must be inferred instead. Downside as a benchmark substrate: continuous
floating-point state makes "exact grading" and cheap replay harder than a discrete integer-state
CA; also computationally heavier than 1-D or lattice-gas CA.

## 5. Sandpile / self-organized criticality — a substrate whose "law" is a broken power law by design

- **Introduction to the Sandpile Model**, review, https://arxiv.org/html/cond-mat/9801182, and
  **The Bak-Tang-Wiesenfeld Sandpile**, https://socsim.readthedocs.io/en/latest/BTW.html — Say:
  each cell holds an integer sand count; above a threshold (4 on a 2-D grid) a cell topples,
  distributing one grain to each neighbor; total sand is exactly conserved in the bulk (only lost
  at open boundaries). Repeated random addition drives the system, without any tuning, into a
  statistically stationary "critical" state where avalanche sizes follow a power law with no
  characteristic scale — this is the defining phenomenon of self-organized criticality (SOC).
- **Self-organised dynamics beyond scaling of avalanches**, https://arxiv.org/pdf/2403.15859, and
  **Signatures of self-organized dynamics in rapidly driven critical sandpiles**, Phys Rev E 110,
  054203, https://link.aps.org/doi/10.1103/PhysRevE.110.054203 — Say: under fast/strong driving
  (departing from the idealized "add one grain, wait for full relaxation" separation of timescales)
  the clean power-law/SOC picture breaks down and gives way to different avalanche statistics —
  i.e. the "SOC law" itself is a regime-dependent effective description, not universal, and the
  literature explicitly studies where and how it fails as driving rate changes.

**Layers reading**: this is close to inverted from lattice gas — the "simple emergent law" IS the
scale-free/critical-exponent statistical law, discoverable only by an agent that runs many
avalanches and fits a distribution (a genuinely statistical discovery task, not a single-trajectory
one); the reachable breaking regime is a driving-rate/timescale-separation knob, again a cheap
scalar depth parameter. Conserved quantity (grain count, minus boundary losses) is exact and easy
to check per-step, giatlanet an agent an early easy "law" before the harder statistical law.
Caution: because the emergent law is statistical (a power-law exponent), grading "did the agent
recover the true law" is fuzzier than grading a closed-form conservation law recovery — worth
flagging as a harder-to-grade substrate family.

## 6. Artificial chemistries / reaction systems

- **Artificial Chemistries — A Review**, Dittrich, Ziegler, Banzhaf, Artificial Life 7(3), 2001,
  https://www.cs.mun.ca/~banzhaf/papers/alchemistry_review_MIT.pdf — Says: an artificial chemistry
  is any (molecule set, reaction rule set, reactor algorithm) triple; documented common phenomena
  include self-maintaining sets of reactions ("organizations") that behave as stable higher-level
  objects even though individual molecule populations fluctuate — i.e. emergent, coarse-grained
  stable entities from fine-grained combinatorial rules.
- **Chemical organization theory: towards a theory of constructive dynamical systems**,
  https://arxiv.org/pdf/q-bio/0501016 — Formalizes "organizations" as closed and self-maintaining
  sets of species; proves that the long-run dynamics of a reaction network can be understood by
  finding these organizations, i.e. gives a literal derivable "effective theory" (which
  organization the system is in) sitting on top of raw reaction-rule dynamics.
- **Combinatory Chemistry: Towards a Simple Model of Emergent Evolution**,
  https://arxiv.org/pdf/2003.07916 — A concrete, cheap, discrete constructive artificial chemistry
  (symbolic combinators reacting under simple rewrite rules) used specifically to study open-ended
  emergent complexity growth — closer in spirit to a "generator with a complexity knob" than most
  CA examples.

**Layers reading**: the "simple regime" is life within one organization (stable relative
abundances / closure); the "breaking regime" is a perturbation (introduce a novel molecule/rule
firing) that knocks the system into a different organization — a qualitative regime change
triggered by a discoverable intervention, arguably a cleaner match to "poke it and watch the law
change" than continuous physical analogies. Conserved quantities are less automatic here than in
LGA/BBM (need explicit design, e.g. total symbol count) but can be added by fiat in the reaction
rules.

## 7. Falling-sand / "powder" automata and Particle Life — weaker on rigor, useful as color

- **Interactive Particle Life Simulation**, https://bionichaos.com/particlelifesim/, and **How a
  life-like system emerges from a simplistic particle motion law**, Nature Scientific Reports,
  https://www.nature.com/articles/srep37969 — The Scientific Reports paper is a primary,
  peer-reviewed source: shows a minimal off-lattice particle model (asymmetric pairwise
  attraction/repulsion, no explicit "life" rules) spontaneously produces motile, cell-like
  aggregates. Useful as evidence that even continuous, non-CA discrete-time particle rules yield
  emergent higher-level objects (motile blobs) cheaply. No literature found (in this pass)
  characterizing a documented *regime where a simple Particle Life "law" provably breaks* — this
  is a gap; flagged as unverified rather than claimed.
- Falling-sand / powder-game style automata (e.g. Noita-style cellular automata) — I could not
  find primary academic literature (only game-dev blog posts, which the brief's rules exclude as
  sources) establishing documented layered-law behavior for this family in this pass. Flagged as
  not verified from a primary source; excluded from strong claims.

## 8. Turing-complete tilings (Wang tiles)

- **An aperiodic set of 11 Wang tiles**, Jeandel & Rao, https://arxiv.org/pdf/1506.06492, and
  general Wang-tile background via https://blog.demofox.org/2016/03/14/computation-with-wang-tile/
  (secondary, for orientation only) — Says: small finite Wang tile sets can be aperiodic (no
  periodic tiling exists) and Turing-complete (can simulate any Turing machine); whether a given
  tile set tiles the plane at all is undecidable in general.
- Relevance to the brief: mainly a warning/limit case rather than a benchmark substrate — a system
  whose "simple regime" is a locally-periodic-looking patch of an aperiodic tiling and whose
  "failure" is global undecidability of long-range structure. Too exotic and too close to
  outright undecidability to be a practical, cheap, gradable benchmark substrate; noted for
  completeness per the assigned angle, not recommended.

## 9. Emerging (2024-2026) work: automated search for interesting automata

- **Automating the Search for Artificial Life with Foundation Models (ASAL)**, Kumar, Lu, Kirsch,
  Tang, Stanley, Isola, Ha (MIT/Sakana AI/OpenAI/IDSIA), arXiv 2412.17799,
  https://arxiv.org/abs/2412.17799 (also https://arxiv.org/html/2412.17799,
  https://github.com/SakanaAI/asal) — Says: uses vision-language foundation models to (1) search
  simulation parameters for a specified target phenomenon, (2) search for parameters producing
  open-ended temporal novelty, and (3) illuminate a whole space of qualitatively distinct
  simulations, tested across Boids, Particle Life, Conway's Game of Life (generalized rule space),
  Lenia, and Neural CA. States it discovered novel CA rules "more open-ended and expressive" than
  the original Game of Life. Relevance: this is direct precedent for treating "rule space of a
  discrete substrate" as a search space to be automatically explored for interesting dynamics —
  i.e. a generator with a knob (rule parameters) that ASAL's method searches; also direct evidence
  that generalized Life-like rule spaces (not just B3/S23) already contain qualitatively different
  regimes worth discovering, supporting a rule-family (not single fixed rule) design for a
  benchmark generator.
- Their choice of substrates (Boids, Particle Life, Life, Lenia, Neural CA) is itself a useful,
  citable shortlist of what current 2024-2026 automated-discovery work treats as tractable,
  interesting substrates — worth reusing/citing when scoping which substrates are already known to
  have rich enough rule spaces to search.

## Comparison table: this substrate family vs. Conway-Life-style grids

| Substrate | Common-regime law | Documented break regime | Conserved/emergent objects | Cost | Reversible/exact grading |
|---|---|---|---|---|---|
| HPP/FHP lattice gas | Navier-Stokes (FHP only) | anisotropy (HPP), high Mach/Re | mass, momentum (exact, by rule) | very low (bitwise) | deterministic, not reversible but exact |
| Margolus/Critters/BBM | ballistic billiards, Life-like gliders | crowding/high density | bijective state map (exact global invariant), ball count/momentum | very low | exactly reversible |
| Rule 54 / Rule 110 (1-D) | uniform "domain" background | glider passage/collision | discrete particle catalog, collision products | extremely low (1-D) | deterministic, mostly irreversible |
| Flow-Lenia | mass-conserving creature kinematics | creature collision, local-parameter boundary | exact total mass; discrete creatures | moderate (float, convolution) | not reversible |
| BTW sandpile | power-law avalanche statistics | fast-driving regime, boundary effects | grain count (near-exact) | low | not reversible; statistical law |
| Artificial chemistry | stable "organization" (closure) | perturbation causing switch of organization | closed/self-maintaining species sets | low-moderate (design-dependent) | not reversible |
| Wang tiles | local periodic-looking patch | global (un)decidable structure | none standard | low but exotic | n/a |
| Conway's Life (baseline) | none derived — patterns classified post hoc, no principled "common regime" theory that predicts most configurations | irreversible everywhere; "failure" isn't a rare regime, unpredictability is the default | no exact conserved quantity (cell count etc. not conserved); gliders/still-lifes are emergent but not part of a provable calculus | very low | not reversible, not exactly invariant |

Conway-Life is the weakest of these for the benchmark's specific need: it has celebrated emergent
objects (gliders, guns) but the literature does not give it a derivable macroscopic "law" that
holds in a common regime and provably fails in a rare one, nor an exact conserved quantity. Every
other substrate in this list was chosen by its original authors specifically because it does have
one or both of those properties, documented in a primary source above.

## 5 concrete world-design ideas (traceable to sources)

1. **Symmetry-as-depth-knob lattice gas.** Generate the world as a block/lattice gas on a
   configurable-symmetry lattice (square → hex/triangular family). Low symmetry = HPP-like,
   visibly anisotropic effective law almost everywhere (shallow theory fails constantly, hard
   mode); high symmetry = FHP-like, Navier-Stokes-style effective law holding broadly, breaking
   only at high injected momentum/density (easy mode with a rare, reachable anomaly). Depth knob =
   a discrete lattice-symmetry/collision-rule parameter. Sourced from Frisch-Hasslacher-Pomeau 1986
   (https://link.aps.org/pdf/10.1103/PhysRevLett.56.1505) and the HPP/FHP comparison in
   https://en.wikipedia.org/wiki/Lattice_gas_automaton.

2. **Reversible block-CA with a hidden bijection as ground truth.** Use a Margolus-neighbourhood
   CA (Critters-family) so the generator can plant an *exact*, checkable invariant (the global
   update is a bijection; local conserved counts in Billiard-Ball-Model variants) that never
   breaks, contrasted with a second, non-conserved quantity that only looks conserved in sparse
   regimes and visibly fails once density/interventions push local blocks into collision. Sourced
   from https://en.wikipedia.org/wiki/Critters_(cellular_automaton) and the Billiard Ball Model
   chapter (https://link.springer.com/chapter/10.1007/978-1-4471-0129-1_6).

3. **1-D particle-catalog worlds with rule-family difficulty knob.** Build worlds on 1-D CA rule
   families (à la Rule 54/Rule 110) where the "shallow theory" is "background domain is static
   (or periodic)" and the deeper truth is a small, enumerable glider/collision grammar. Depth knob
   = number of distinct domains + glider species reachable from the chosen rule; agent must run
   long enough or intervene (inject a defect) to see a collision and infer the rulebook. Sourced
   from the Rule 54 particle-catalog analysis (https://csc.ucdavis.edu/~cmg/papers/ECA54.pdf) and
   the Hordijk-Shalizi-Crutchfield bound on collision products (https://arxiv.org/pdf/nlin/0008038).

4. **Locally-heterogeneous mass-conserving field with planted anomaly patch.** Use a Flow-Lenia-
   style field where the update rule's parameters are spatially localized; the generator plants a
   small region with different local parameters (a different "physics patch") inside an otherwise
   uniform world. Common regime: single global convolution kernel predicts creature behavior
   everywhere except that patch. Depth knob = patch size/contrast. Mass conservation gives an exact
   invariant to check globally. Sourced from Flow-Lenia (https://arxiv.org/abs/2506.08569,
   https://arxiv.org/pdf/2212.07906).

5. **Driving-rate knob on a sandpile for statistical-law discovery tasks.** Use a BTW-style
   sandpile where the driving rate (grains added per relaxation-time) is the depth knob: slow
   driving gives the classic scale-free avalanche law (the "simple regime" the agent must recover
   by running many trials and fitting a distribution); fast/strong driving is a reachable regime
   documented to depart from clean SOC statistics. This is deliberately different in *kind* from
   the other four (statistical law rather than closed-form conservation law) and would test whether
   agents can recognize when the right "theory" to submit is a distribution/exponent rather than an
   equation. Sourced from https://arxiv.org/html/cond-mat/9801182 and
   https://link.aps.org/doi/10.1103/PhysRevE.110.054203.

## Objections and warnings raised in the literature (or by inference, marked as such)

- **Statistical noise (sourced)**: LGA/HPP/FHP models are documented to have significant intrinsic
  statistical noise from boolean occupation variables (https://arxiv.org/pdf/comp-gas/9905001),
  which is exactly why Lattice Boltzmann replaced them for practical fluid simulation. If the
  benchmark needs an agent to recover a clean closed-form law from a small number of runs, raw
  boolean LGA may require substantial spatial/temporal averaging first — a hidden difficulty cost,
  not visible from the rule description alone.
- **SOC universality is not universal (sourced)**: recent papers (2024) explicitly show the
  clean sandpile power-law breaks under different driving regimes/timescale separations
  (https://arxiv.org/pdf/2403.15859, https://link.aps.org/doi/10.1103/PhysRevE.110.054203) — good
  for the brief's "reachable failure" requirement, but also a warning that "the law" itself may be
  an idealization that only exactly holds in a limit, making exact grading of a submitted law
  harder for this substrate family than for exact-conservation substrates.
- **Grading difficulty gradient (my inference, not sourced)**: substrates differ a lot in how easy
  it is to write an automated exact grader. Exact-conservation substrates (LGA momentum/mass,
  BBM ball count, Flow-Lenia mass, sandpile grain count) give a trivially checkable invariant.
  Statistical-law substrates (SOC exponent) and organization-theoretic substrates (artificial
  chemistry) require fitting/inference to grade, which is more expensive and less exact — this is
  an inference, not something any source states directly, but it follows from comparing how each
  paper actually validates its own claimed law (closed-form derivation for LGA vs. curve-fitting
  histograms for SOC).
- **Particle Life and falling-sand automata are under-verified for this angle (flagged)**: I found
  a primary peer-reviewed source for minimal particle-motion emergent structure (Scientific
  Reports, https://www.nature.com/articles/srep37969), but no primary source in this pass
  documenting a *specific, reachable regime where a simple Particle-Life law provably breaks* —
  unlike LGA/sandpile/Rule54, where the breaking regime is explicitly characterized in the
  literature. Do not treat Particle Life as equally well-grounded for the "law breaks in a
  reachable regime" requirement without further search.
- **Wang tiles are a poor fit despite being "layered" in a technical sense (my inference)**: the
  undecidability results (https://arxiv.org/pdf/1506.06492) mean that in the worst case there is no
  finite experiment that tells an agent whether the "locally periodic" theory ever breaks — this
  is the opposite of what a gradable, terminating benchmark task needs, so this substrate should be
  avoided even though it technically has nested regimes of apparent order and disorder.
