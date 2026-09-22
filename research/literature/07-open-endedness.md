# Open-endedness for a single-agent, bounded, exact-match discovery benchmark

Scope note: this brief only uses claims from sources actually fetched and read this
session. Every claim below is tagged "[source says, URL]" or "[my inference]". Where
a source's page only exposed an abstract and a summarization tool could not get the
full formal content, that is noted rather than filled in from memory.

Sources actually opened this session:
- Hughes et al. 2024, "Open-Endedness is Essential for Artificial Superhuman
  Intelligence" — https://arxiv.org/html/2406.04268 (HTML version, full text)
- Stanley, Lehman, Soros, "Open-Endedness: The Last Grand Challenge You've Never
  Heard Of" — https://www.oreilly.com/radar/open-endedness-the-last-grand-challenge-youve-never-heard-of/
- Jiang, Rocktäschel, Grefenstette, "General Intelligence Requires Rethinking
  Exploration" — https://arxiv.org/html/2211.07819v1
- Wang, Lehman, Clune, Stanley, POET — https://arxiv.org/abs/1901.01753 (abstract only;
  full formal ingredient list not confirmed beyond the abstract)
- Faldor, Zhang, Cully, Clune, OMNI-EPIC — https://arxiv.org/html/2405.15568v2 (full text)
- Kumar, Lu, Kirsch, Tang, Stanley, Isola, Ha, ASAL — https://arxiv.org/html/2412.17799
  (full text)
- Lu, Hu, Clune, "Automated Capability Discovery" — https://arxiv.org/html/2502.07577
  (full text)
- Clune, "AI-GAs" — https://arxiv.org/abs/1905.10985 (abstract-level only; three-pillars
  claim is from the search summary of the abstract, not independently re-verified against
  full text this session)

Not obtained despite trying: the precise mathematical text of Hughes et al.'s definitions
was recovered from the HTML fetch tool's summarized rendering, not by reading raw LaTeX,
so the equations below should be treated as a faithful paraphrase, not a verbatim quote.
Novelty search original papers (Lehman & Stanley) and a distinct 2025-2026
evaluation-specific open-endedness paper were searched for but not found/opened as a
readable primary source this session — flagged as gaps below rather than filled in.

---

## 1. Formal definition of open-endedness, and whether a finite world can satisfy it

**What the source says.** Hughes et al. give the definition that matters most for us:
open-endedness is a property of a *sequence of artifacts produced by a system, relative
to an observer O*. The observer keeps a predictive model over the artifact sequence with
a loss function ℓ. The system is open-ended iff the sequence is simultaneously:

- **Novel**: for any time t and any horizon T beyond t, there is always a later time T'
  at which the observer's predictive loss is higher than at T — i.e., surprise keeps
  recurring rather than saturating.
- **Learnable**: conditioning the observer's model on a longer history of the past
  reduces its loss on the near future — i.e., the observer keeps getting better at
  prediction by having watched more.
(https://arxiv.org/html/2406.04268)

Both conditions must hold together. Novelty alone (a system that keeps surprising the
observer but never rewards longer observation with better prediction) is not
open-ended — their canonical counterexample is a TV switched to random channels: always
surprising, never learnable (https://arxiv.org/html/2406.04268).

Crucially, the paper **explicitly distinguishes infinite from finite open-endedness**:
a system can be "infinitely open-ended" (the novelty+learnability conditions hold as the
time horizon τ→∞) or merely "finitely open-ended" (they hold only for bounded t,T<τ).
They state that existing systems such as AlphaGo and Adaptive Agent (AdA) exhibit only
finite open-endedness — novelty plateaus within practical timescales — and treat this as
a reflection of real computational/temporal constraints, **not a theoretical
impossibility within a bounded space** (https://arxiv.org/html/2406.04268).

Stanley/Lehman/Soros's earlier framing is compatible but stricter in spirit: they define
open-endedness as a process that "tirelessly invents ever-greater complexity and
novelty across incomprehensible spans of time," and explicitly flag that existing
novelty-search/quality-diversity algorithms are confined to *finite possibility spaces*
and plateau once those are exhausted — "there are only so many interesting ways you can
walk before it just starts being silly." True (unbounded) open-endedness, in their view,
requires the solution space itself to expand, not just be explored
(https://www.oreilly.com/radar/open-endedness-the-last-grand-challenge-youve-never-heard-of/).

**My inference.** Our world (fixed HPP-lattice-gas rules, finite grid, finite cell
states, finitely many floors) can only ever be *finitely* open-ended in Hughes et al.'s
sense, and this is fine — their own examples of open-ended-enough-to-matter systems
(AlphaGo, AdA) are also finite/bounded and only finitely open-ended. What we need is not
infinite open-endedness but that, relative to the agent as observer, the loss curve over
the RUN/POKE/SUBMIT sequence stays high for long enough (novel) and drops meaningfully
with more interaction (learnable) across the budget we grant. This reframes "is floor 3
worth having" as an empirical question: does an agent's predictive loss on held-out
frames keep finding new surprises as it pokes deeper (novelty), and does its loss
actually fall as it accumulates pokes (learnability)? If pokes stop reducing loss before
budget exhaustion, the world is not open-ended for that agent at that budget — it is
just hard. If the same collision always looks the same, no matter how it is poked, and
the loss floor is reached in one or two well-chosen interventions, the world was never
open-ended, it was a one-shot puzzle. The novelty side is what our depth-knob (floors 1-3
each needing to be reached by poking) is trying to guarantee.

## 2. How open-endedness is turned into something measurable — proxies and failure modes

**What the sources say.**

- Hughes et al.'s own definitions above (novelty as recurring loss increase, learnability
  as loss decrease with more history) ARE already the proposed measurement recipe: pick
  an observer model class and loss function, then track its loss curve over time
  (https://arxiv.org/html/2406.04268). They note the observer's *choice of loss function*
  is where "interestingness" gets smuggled in — different observers find different
  things salient, so the metric is observer-relative by construction, not
  observer-independent (https://arxiv.org/html/2406.04268).

- Jiang, Rocktäschel and Grefenstette's proxies for "which training data is worth
  seeking" include epistemic uncertainty (prediction variance / ensemble disagreement),
  state-visitation-frequency-based novelty, raw prediction error, regret, and their
  preferred composite, "learning potential," which they decompose into three required
  properties: **improvability** (there is room to get better), **learnability** (the
  agent can efficiently improve given more exposure), and **consistency** (the "solution"
  to a given environment configuration doesn't keep changing under you)
  (https://arxiv.org/html/2211.07819v1). They flag a specific, named failure mode:
  **"stochastic traps"** — regions of high irreducible (aleatoric) noise that look
  informative to naive novelty/uncertainty proxies but never actually teach the agent
  anything, because the noise is not reducible by more data. Their fix is to explicitly
  model aleatoric vs epistemic uncertainty or average learning-potential over batches of
  trajectories (https://arxiv.org/html/2211.07819v1).

- OMNI-EPIC operationalizes "interestingness" by outsourcing it entirely to a foundation
  model judge: an LLM proposes new tasks conditioned on an archive, and a second
  "post-generation model of interestingness" checks the new proposal against its nearest
  neighbors in the archive for whether it's "novel, surprising, diverse, worthwhile"
  (https://arxiv.org/html/2405.15568v2). Documented weak spots: current VLMs are "not yet
  accurate enough" to be trusted as success detectors, and the authors note prior related
  work "encountered pathologies when optimizing against definitions of interestingness"
  (i.e., a system can learn to game an interestingness judge), though OMNI-EPIC itself
  does not present a worked example of this happening to them specifically
  (https://arxiv.org/html/2405.15568v2).

- ASAL turns open-endedness into a concrete number for finite cellular automata: it
  minimizes, over rule parameters θ, the expected maximum similarity (in a
  vision-language foundation model's embedding space) between the current simulation
  frame and any earlier frame in the same run — i.e., it rewards states that look
  unlike every prior state, per an external FM's notion of "looks different"
  (https://arxiv.org/html/2412.17799). They are explicit that this "outsources the
  subjectivity of measuring open-endedness to the construction of the [FM] representation
  function" — the metric is only as good as the embedding space's notion of similarity,
  and no CA is open-ended "in itself," only relative to that chosen observer
  (https://arxiv.org/html/2412.17799).

- Automated Capability Discovery uses a cheaper, more brittle proxy: a text-embedding
  nearest-neighbor filter plus an LLM gate asking whether a newly proposed evaluation
  task is "interestingly new" relative to its neighbors (https://arxiv.org/html/2502.07577).
  It does **not** connect this to Hughes et al.'s novelty+learnability framework at all —
  it is a much shallower proxy (embedding dissimilarity + one LLM judgment), and the
  paper documents the judge has "a slight positive bias (more false positives than false
  negatives)" and performs worse specifically on the hardest ("Very Difficult") tasks
  (https://arxiv.org/html/2502.07577).

**My inference.** All four measurable proxies found in the literature — recurring
predictive surprise, learning-potential (improvability × learnability × consistency),
FM-embedding novelty, and LLM-judged "interestingly new" — share one structural risk for
us: they are all defined relative to some proxy observer (a model, an embedding space, an
LLM judge), and every source that discusses this explicitly names gaming/degeneracy as
the corresponding failure mode (stochastic traps in Jiang et al.; "pathologies when
optimizing against definitions of interestingness" in OMNI-EPIC; embedding-space bias in
ASAL; judge bias in ACD). Our benchmark is safer than all of these because our proxy
observer is not a fuzzy learned model — it is exact frame-for-frame ground-truth
matching. That sidesteps judge-gaming almost entirely, but it also means we get none of
the "graceful partial credit / interestingness signal" these proxies provide; our
novelty/learnability curve has to be read off submit-attempt error rates and poke
efficiency rather than off a smooth loss, which is a genuine design gap the literature
does not solve for us (see recommendation 3 below).

## 3. Is mimicking open-ended discovery inside a bounded benchmark coherent, and what's the minimum ingredient list?

**What the sources say.**

- Hughes et al.'s own framing already answers "is it coherent": yes, in the *finite*
  sense — see Q1. They do not claim bounded systems are lesser or fake instances of
  open-endedness, only that they saturate sooner (https://arxiv.org/html/2406.04268).

- Jiang et al. draw a sharper line that is more skeptical of bounded environments for
  *training* open-endedness: "A static simulator with adjustable parameters can span a
  vast space of tasks, [but] ultimately, it can only offer experiences within the limited
  domain that it was designed to simulate." They contrast **prioritized training**
  (choosing which of a fixed set of pre-existing tasks/data to focus on) against **active
  collection** (continually creating genuinely new tasks/MDPs), and argue that even
  sophisticated methods confined to a parameterized MDP space (their example:
  Unsupervised Environment Design) do not achieve true open-endedness because the
  configuration space itself is fixed (https://arxiv.org/html/2211.07819v1).

- POET's abstract gives what is, in effect, the minimal-ingredient list for open-ended
  *training*: (1) a mechanism that keeps generating new environmental challenges, (2) a
  population of agents that improve on those environments, and (3) transfer of solutions
  between environments so that "stepping stones" found for one challenge unlock progress
  on another; POET explicitly claims that without this open-ended, coupled
  generate-and-solve loop, some challenges are unsolvable "by direct optimization alone,
  or even through a direct-path curriculum-building control algorithm" — i.e. a fixed
  linear curriculum is provably insufficient in their tested domains (https://arxiv.org/abs/1901.01753).

**My inference (this is the crux question and needs care).** Our benchmark is explicitly
NOT trying to train an open-ended learner — it is evaluating whether a fixed agent can
discover a fixed, already-designed-in structure once, under budget. None of these
sources are about that case; POET and Jiang et al. are about a system that must keep
GENERATING new content, which we deliberately don't do (our floors are hand-designed and
finite by the brief's own framing). The honest reading of the literature is: "open-ended
discovery" and "a hard, deep, one-shot discovery task in a fixed world" are different
things, and the open-endedness literature's minimum ingredient list (generator that keeps
producing learnable novelty + agent that transfers stepping stones + no fixed
representation handed to the agent) is a recipe for the FIRST, not a certification
requirement for the SECOND. What we can legitimately borrow, translating "keeps
producing learnable novelty" from a population/generation setting into a single-episode
poke/submit setting, is:
  (a) the world itself, not the benchmark harness, must be the source of the "generator"
      — each floor's hidden structure plays the role POET's environment-generator plays,
      except pre-committed rather than adaptively invented;
  (b) the agent must not be handed the state representation for floor 2/3 (visible
      cell contents only, not the hidden inner-state variable) — this is the direct analog
      of Jiang et al.'s point that the agent, not the designer, must discover the
      structure of the space it operates in, otherwise there is no discovery, only fitting;
  (c) "transfer of stepping stones" has a natural analog in our poke interface: a
      hypothesis formed from floor-1 behavior should be reusable (falsifiable, extendable)
      when probing floor 2 — if the interface forces the agent to discard everything and
      restart per floor, we've broken the one piece of POET's machinery that plausibly
      transfers.
This is inference, not something asserted in any fetched source — flagged as such.

## 4. Reward structure for a future RL-environment version, without collapsing to a fixed objective

**What the sources say.**

- Hughes et al. sketch four *non-exclusive* directions rather than one reward recipe:
  RL with foundation-model-guided exploration toward "human-relevant" artifacts;
  self-improvement loops where the model generates and evaluates its own hypotheses;
  task generation that maintains difficulty inside the learner's zone of proximal
  development; and evolutionary methods using LLMs as mutation/selection operators
  (https://arxiv.org/html/2406.04268).

- Jiang et al.'s "learning potential" (improvability × learnability × consistency) is the
  most concrete, portable reward signal in the set: reward the agent (or reward the
  curriculum-generator) for choosing situations where the agent is currently wrong but
  can become less wrong with more data, discounting situations dominated by irreducible
  noise ("stochastic traps") (https://arxiv.org/html/2211.07819v1).

- OMNI-EPIC's concrete mechanism is a **curriculum built from an archive of past
  successes/failures**: the task generator is explicitly conditioned on what has already
  been tried, and a novelty-vs-archive check gates new tasks — i.e., the reward for
  "generate a new task" is implicitly shaped by dissimilarity to the archive, not by
  raw task difficulty (https://arxiv.org/html/2405.15568v2).

**My inference.** For our eventual RL-environment framing, the closest defensible
translation, chaining each source's mechanism to our poke/submit interface, is:
  - per-step reward should NOT be "distance to ground truth," which collapses to a fixed
    objective the moment the agent overfits visible behavior — the exact-match SUBMIT
    grade should stay a terminal/sparse signal (this is where "exact-match grading" is a
    feature, not a bug, versus the smoothed proxies these sources use, all of which they
    also flag as gameable);
  - the intermediate (per-poke) reward should be Jiang et al.'s learning-potential
    triple, instrumented concretely as: did the agent's own held-out prediction error
    (on frames it hasn't poked) go down after this poke (learnability), was there room
    for it to go down (improvability — not already near a noise floor), and is the
    lesson stable across repeats of a similar poke (consistency, ruling out
    stochastic-trap pokes like re-triggering the same collision under sensor noise)
    (https://arxiv.org/html/2211.07819v1);
  - a curriculum-from-failed-submits, in the spirit of OMNI-EPIC's archive-conditioned
    generation, means: a failed SUBMIT should reveal (or make cheaply discoverable)
    *which held-out situations it failed on*, functioning like OMNI-EPIC's
    novelty-vs-archive check — pushing the agent toward the specific unresolved floor
    rather than toward re-deriving the whole theory from scratch
    (https://arxiv.org/html/2405.15568v2).
This is a design proposal built by analogy, not something any source states for our
setting — flagged as inference throughout.

## 5. Documented stagnation/gaming failure modes, and what they'd look like in OUR world

**What the sources say, each with a named mechanism:**

- **Noisy-TV problem** (novelty without learnability): a system that produces endless
  surprise but no compressible structure (https://arxiv.org/html/2406.04268).
- **Stochastic traps** (an exploration/reward-seeking process gets stuck chasing
  irreducible noise because naive novelty/uncertainty proxies can't distinguish
  "genuinely informative" from "genuinely random") (https://arxiv.org/html/2211.07819v1).
- **Plateauing in a finite possibility space**: novelty-search-style methods exhaust a
  bounded space of variations and stop producing anything new — "there are only so many
  interesting ways you can walk before it just starts being silly"
  (https://www.oreilly.com/radar/open-endedness-the-last-grand-challenge-youve-never-heard-of/).
- **Gaming/exploiting the interestingness judge**: OMNI-EPIC cites that prior related
  work saw "pathologies when optimizing against definitions of interestingness," and
  separately flags that current VLM success-detectors are not accurate enough to be
  trusted (https://arxiv.org/html/2405.15568v2).
- **Judge/observer bias in the metric itself**: ASAL's novelty score is entirely a
  function of the chosen FM embedding space, and the authors admit the metric's validity
  is inherited wholesale from that representation's biases, with no independent check
  (https://arxiv.org/html/2412.17799). ACD's LLM judge is shown to have "a slight
  positive bias (more false positives than false negatives)" and specifically degrades
  on the hardest tasks (https://arxiv.org/html/2502.07577).
- **Bootstrap collapse in retraining loops**: Jiang et al.'s formal failure mode where a
  model retrained only on data it currently favors converges to a fixed point where the
  induced data distribution equals the training distribution — a self-reinforcing local
  optimum with no new information entering (https://arxiv.org/html/2211.07819v1).

**My inference — concretely mapped onto the HPP lattice gas / hidden-inner-state floors:**

1. *Noisy-TV analog*: an agent that treats every collision outcome as freshly
   unpredictable (never builds a compressed rule) but keeps "poking" indefinitely without
   its predictive error ever dropping — this would show up as an agent that pokes a large
   budget with flat held-out error; per Hughes et al. this is novelty without
   learnability, i.e., not discovery, just noise-sampling. Our grading should catch this
   automatically (SUBMIT will fail), but the RECOVERY score should specifically penalize
   an agent that responds to a failed submit by poking MORE without changing its
   hypothesis, since that is exactly this failure mode enacted post-failure.

2. *Stochastic-trap analog*: floor 3's hidden inner state "flips on certain collisions and
   changes later collisions" and is "only detectable via designed crashes" — this is
   exactly a stochastic-trap risk if the agent cannot distinguish "this crash outcome
   looks weird because of hidden state" from "this crash outcome looks weird because two
   near-simultaneous collisions aliased on the grid" (an artifact of discretization, not
   of the hidden variable). Per Jiang et al., the fix pattern is to make the
   informative signal separable from noise by repeatability: the interface should let an
   agent re-run the *same* designed crash (RUN with identical initial state) and see
   whether the anomaly repeats — if it does, it's structure; if not, it was a discretization
   artifact. If POKE does not support exact state reproduction, floor 3 risks being a
   stochastic trap by construction.

3. *Plateau-in-finite-space analog*: floor 1 ("balls fly straight" fits) is a small,
   fast-exhausted hypothesis space — an agent that gets floor 1 right can then plateau if
   floor 2's crowded regime doesn't force a visibly different, learnable improvement
   within budget (e.g., collisions are rare enough in the test suite that the floor-1
   theory still scores acceptably on held-out situations). This is the Stanley/Lehman
   "silly variations" plateau, but for us it's a benchmark-construction risk, not an
   algorithmic one: if held-out situations under-sample crowded regimes, the benchmark
   itself fails to reward moving past floor 1, defeating the "depth knob" design intent.

4. *Judge/metric gaming analog*: because our grading is exact-match against ground truth
   (not an FM/LLM judge), the ACD/ASAL failure mode of "gaming a biased judge" does not
   transfer directly to SUBMIT grading. It DOES transfer to any softer, LLM-based
   instrumentation we might add later (e.g., an LLM grading the AGENT's prose theory, or
   an LLM deciding whether a poke was "well-designed") — per ACD, such a judge would
   likely be positively biased and specifically worse at distinguishing genuinely
   floor-3-level submissions from floor-2 submissions dressed up in floor-3 language
   ("Very Difficult" tasks were exactly where ACD's judge degraded)
   (https://arxiv.org/html/2502.07577). Recommendation: keep any judge-based scoring
   (if added) off the headline metric.

5. *Bootstrap-collapse analog*: if the agent's poke-selection policy (in a future
   RL-trained version) is trained against its own current world-model's uncertainty
   estimate, it can converge to only poking situations its own (wrong) model is
   confident about — never discovering the hidden state at all, a direct instance of
   Jiang et al.'s fixed-point collapse (https://arxiv.org/html/2211.07819v1). This is the
   single most relevant warning for the "port to RL later" plan: an intrinsic-reward
   signal computed from the agent's own model, with no external ground-truth anchor
   until SUBMIT, has exactly the topology needed for this collapse.

---

## Concrete design recommendations

1. **Instrument novelty/learnability as two separate curves per world**, following
   Hughes et al.'s definition directly: track the agent's held-out predictive loss over
   the poke sequence; require it to (a) keep finding situations where loss spikes as it
   goes deeper (novelty — evidence a floor exists) and (b) show loss trending down as
   poke count grows (learnability — evidence the floor is learnable within budget). A
   world/floor combination that fails either curve in pilot testing is not doing its job.
   (Source: https://arxiv.org/html/2406.04268)

2. **Guard floor 3 against being a stochastic trap** by making the POKE interface support
   exact state reproduction (same seed / same edited cells → identical re-run), so an
   agent can test "is this weirdness structure or discretization noise" the way Jiang et
   al.'s learning-potential framework requires distinguishing epistemic from aleatoric
   uncertainty. (Source: https://arxiv.org/html/2211.07819v1)

3. **Keep exact-match SUBMIT grading as the terminal signal and resist adding an
   LLM/embedding "interestingness" or partial-credit judge to the headline score.** Every
   source that used a learned/FM-based novelty or interestingness proxy (OMNI-EPIC, ASAL,
   ACD) also reported that the proxy inherits its judge's biases and is potentially
   gameable; our exact-match design already avoids this class of failure and should not
   reintroduce it. (Sources: https://arxiv.org/html/2405.15568v2,
   https://arxiv.org/html/2412.17799, https://arxiv.org/html/2502.07577)

4. **Let a failed SUBMIT reveal which held-out situations it failed on** (not just
   pass/fail), giving the agent an archive-conditioned next target the way OMNI-EPIC
   conditions new task generation on what's already been tried/succeeded/failed — this
   is the direct translation of "curriculum from failed submits" into our interface.
   (Source: https://arxiv.org/html/2405.15568v2)

5. **Preserve hypothesis continuity across floors in the interface** (a floor-1 theory
   should be extendable/falsifiable when the agent starts probing floor 2, not discarded
   and restarted), as the nearest analog to POET's requirement that stepping-stone
   solutions transfer across environments rather than be solved from scratch each time.
   (Source: https://arxiv.org/abs/1901.01753 — abstract-level claim, not independently
   verified against full text this session)

6. **If a future RL-trained poke-policy uses intrinsic/learning-potential reward, anchor
   it periodically against ground truth (even coarsely), not purely against the agent's
   own model's self-assessed uncertainty**, to avoid the bootstrap fixed-point collapse
   Jiang et al. describe, where a model trained only on data it currently favors stops
   receiving new information entirely. (Source: https://arxiv.org/html/2211.07819v1)

7. **Treat "finite open-endedness" as the honest, sufficient target, not a compromise.**
   Hughes et al. state existing systems (AlphaGo, AdA) are only finitely open-ended and
   still count as meaningful cases; our HPP world with 2-3 floors should be justified as
   "open-ended enough for the budget we grant," not apologized for as "not really
   open-ended because it's finite." (Source: https://arxiv.org/html/2406.04268)

## Strongest warnings

- **Floor 3 is the highest-risk stochastic-trap candidate in this design.** A hidden
  variable "only detectable via designed crashes" is precisely the situation Jiang et
  al. warn produces false learning signal if the agent (or its poke-selection reward)
  cannot tell structured surprise from grid-discretization noise or from rare aliasing of
  two near-simultaneous collisions. Without exact-repeat capability in POKE, this floor
  risks either being unsolvable-by-design (looks like noise, budget wasted) or
  accidentally solvable by memorizing specific numeric coincidences rather than genuine
  structure. (https://arxiv.org/html/2211.07819v1)

- **Exact-match grading removes judge-gaming risk from SUBMIT, but any softer metric
  layered on top (LLM-graded theory writeups, embedding-based poke-quality scores,
  "interestingness" of an agent's chosen crashes) reintroduces exactly the bias/gaming
  failure modes reported for OMNI-EPIC, ASAL, and ACD.** Keep those, if used at all,
  diagnostic-only and off the headline percent-solved metric.
  (https://arxiv.org/html/2405.15568v2, https://arxiv.org/html/2412.17799,
  https://arxiv.org/html/2502.07577)

- **A shallow theory can survive if the held-out test suite under-samples the regime that
  would falsify it** — the literature's "plateau in a finite space" warning becomes, for
  us, a benchmark-construction risk rather than an agent-side one: if crowded-regime or
  hidden-state-triggering situations are rare among held-out situations, a floor-1 or
  floor-2 theory can still score well, and the depth knob silently stops discriminating.
  (https://www.oreilly.com/radar/open-endedness-the-last-grand-challenge-youve-never-heard-of/)

- **Porting to RL later inherits the bootstrap-collapse risk specifically**: any
  intrinsic/learning-potential reward computed purely from the agent's own current
  world-model (rather than periodically checked against ground truth) can converge to a
  fixed point where the agent stops seeking the very evidence (rare crashes) that would
  reveal floor 2/3, because its own model is "confident" (wrongly) in the region it
  already samples. (https://arxiv.org/html/2211.07819v1)

## Gaps / not covered

- Novelty search's original formal papers (Lehman & Stanley) were not located as a
  distinct readable primary source this session (searches surfaced only the Stanley/
  Lehman/Soros essay, which does discuss novelty search but is not the original paper);
  no claim above is attributed to the original novelty-search paper.
- No 2025-2026 paper defining or measuring open-endedness specifically FOR EVALUATION
  (as opposed to training) was found as a distinct primary source; ACD is the closest
  fit and is treated as such, but it does not itself claim to formalize
  "open-endedness-as-evaluation-property" the way Hughes et al. formalize
  open-endedness-as-training-property.
- "Picbreeder with VLMs"-style 2025-2026 work was searched for implicitly via ASAL-adjacent
  queries but not separately opened; not represented in this brief.
- AI-GAs and POET claims above rely on abstract-level content only (the fetch tool
  returned abstract-only pages); their "Three Pillars" and "minimum ingredients" framing
  should be treated as provisional until the full text is read.
