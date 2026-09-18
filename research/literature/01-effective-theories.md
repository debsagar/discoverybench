# Effective theories and layered laws in rule-based discrete worlds

Angle: physics and philosophy of science on why simple laws hold in one regime and
break in another, applied to the question of how to *build* a discrete, deterministic,
generated world that has this property baked into its structure rather than
scripted in.

## Key question restated

What structural feature of a rule-based discrete world makes a simple approximate
law valid in one regime and invalid in another, and what is the small
parameter/limit that controls the crossover?

## Sources actually read

### 1. Israeli & Goldenfeld, "Coarse-graining of cellular automata, emergence, and
the predictability of complex systems," Phys. Rev. E 73, 026203 (2006);
earlier version "On computational irreducibility and the predictability of complex
physical systems," arXiv:nlin/0309047.
- URL (arXiv full text, fetched): https://arxiv.org/html/nlin/0309047
- URL (published PDF, located but not machine-readable as text): https://guava.physics.ucsd.edu/~nigel/REPRINTS/2006/Israeli%20Coarse-graining%20of%20cellular%20automata%20PRE%202006%20(PDF).pdf

**What the paper says.** They take elementary cellular automata (ECA) and build an
explicit renormalization-group-style coarse-graining procedure:
1. Group N adjacent cells into a "block," giving a fine-scale alphabet of size S^N.
2. Choose a projection map P from the fine alphabet down to a coarse alphabet
   (e.g., "is this block all 1s?" or "parity of the block").
3. Ask whether there exists a coarse-grained update rule f̄ such that evolving the
   fine CA one step and then projecting equals projecting first and then applying
   f̄. This is a **self-consistency condition**:
   f̄(P(x1),P(x2),P(x3)) must be well-defined — i.e., any two fine-scale
   neighborhoods x, y that project to the same coarse value at every cell must
   also lead to the same coarse successor. If two fine configurations agree after
   projection but diverge after one more step, f̄ is multi-valued and no exact
   deterministic coarse law exists at that (N, P).

**Concrete results (what the paper reports, not my inference):**
- Some Class 3 (chaotic-looking) rules coarse-grain to *simple* fixed or
  low-complexity coarse rules with small block size (e.g. one example collapses
  a rule to a trivial constant/steady-state rule at N=3).
- Rule 110 (proved Turing-universal, i.e. maximally computationally irreducible at
  the microscopic level) still admits *exact* coarse-grained deterministic
  descriptions once N is taken large enough (N=5,6,7+) with an appropriately chosen,
  non-injective projection — the coarse-grained automaton reproduces exactly the
  large-scale motion of Rule 110's "gliders"/particles without simulating every
  microscopic bit.
- A handful of rules (30, 45, 106, and symmetric variants) resisted the authors'
  coarse-graining attempts at the block sizes they tried — they could not find any
  N, P for which the self-consistency condition held, i.e. no simple coarse law
  was found (though the authors flag this could be a limit of their search, not a
  proof of impossibility).
- For N ≤ 4 the found reductions form a partial order: coarse-graining never
  increases apparent complexity, suggesting a genuine hierarchy of levels of
  description, not an arbitrary rewriting.
- Framing: computational irreducibility, in Wolfram's sense, is a *microscopic,
  fine-grained* property. It does not imply irreducibility of every
  coarse-grained projection of the same system. Whether a given macroscopic
  observable admits a simple update law is a separate, scale-dependent question:
  it depends on which projection operator you use, i.e. which coarse degrees of
  freedom you choose to track.

**Why it matters for us.** This is the single most load-bearing paper for the
benchmark design. It gives a mechanistic, constructive account (not just an
analogy) of exactly the property we want: a discrete deterministic microscopic
rule that (a) has no shortcut at the fine scale (irreducible/chaotic/universal),
yet (b) has an *exact*, simple, and cheap-to-compute law at a coarser scale, for
*some* choices of scale and coarse variable and not others. The controlling
"knob" here is explicit and mechanical: **block size N (spatial coarse-graining
scale) and the choice of projection P**. Both are literal parameters you can put
in a generator.

### 2. Effective field theory (EFT) / renormalization group in physics — general
review material.
- URLs: https://link.springer.com/article/10.1007/BF01063904 (Bain/Castellani-type
  "The renormalisation group and effective field theories," Synthese);
  https://arxiv.org/html/2507.17573v1 ("Renormalization group for effective field
  theories: cutoff schemes and universality"); background summary via search.

**What this literature says.** An EFT is valid below some energy/momentum cutoff
Λ (equivalently, above some length scale 1/Λ). Below the cutoff, only a finite set
of "relevant" and "marginal" operators/degrees of freedom matter; everything from
shorter distances/higher energies is either integrated out or suppressed by
powers of (E/Λ). The controlling small parameter is a ratio of scales: (probe
energy)/(cutoff energy), or equivalently (microscopic length)/(macroscopic
length). As you push a probe toward Λ (higher energy, finer resolution, faster
processes, shorter time/length scales), the suppressed operators stop being
negligible and the "simple" low-energy law visibly fails — not gradually into
nonsense, but into specific, calculable corrections that point to the next layer
of theory. This is presented as *generic*: any theory with a separation of scales
looks this way, and the renormalization group is the tool that tracks how the
"effective" couplings drift as you change the scale at which you look
(coarse-graining in momentum/energy space, structurally the same operation as
Israeli & Goldenfeld's block-spin coarse-graining in position space).

**Why it matters.** This gives the general theory of which Israeli-Goldenfeld's
CA result is a discrete, exactly-solvable special case. It says the *type* of
small parameter that should gate our world's "depth" knob is a **scale ratio**:
(resolution or energy or speed of the intervention) divided by (a cutoff intrinsic
to the world's construction). This generalizes beyond CA cell-blocks to any
generator: e.g., simulation step size vs. some intrinsic correlation length,
intervention magnitude vs. a saturation threshold, or observation rate vs. a
built-in refresh/mixing rate.

### 3. Correspondence principle (Bohr; philosophy of science).
- URL: https://plato.stanford.edu/entries/bohr-correspondence/

**What it says.** The generalized correspondence principle (Post 1971, as
summarized by SEP) requires a new theory to "degenerate into" the old theory
under exactly the conditions where the old theory was empirically well-confirmed.
For quantum-to-classical, the nominal limiting parameter is large quantum number
n → ∞ (Bohr's original case), but SEP flags a real caveat: this reduction is not
a clean limit — it is asymptotic and only statistical, and Post argues the
naive story ("quantum mechanics reduces to classical mechanics as n → ∞") is
literally false in important respects, because quantum emission is single-photon
while classical emission is a continuous simultaneous spectrum. Bohr himself
resisted treating this as merely a mathematical limiting relation, insisting it
was a stronger constraint on any acceptable theory, not just an asymptotic
curiosity.

**Why it matters / caution for us.** Two lessons. (a) A "shallow theory fits,
then a deeper theory replaces it" pair is philosophically well precedented and
named — correspondence is the requirement that this succession isn't arbitrary,
the new law must provably contain the old one as a limit, not just superficially
resemble it. Our depth-2 (or depth-N) generator should have this property: rerunning
the coarse law inside the fine law's validity region should reproduce it exactly
or near-exactly, not just "look similar." (b) the caveat is a genuine warning:
correspondence limits are frequently *not* clean parameter limits but involve a
qualitative change in what kind of object the theory talks about (discrete
photon vs continuous wave). If we want "investigate, revise" to be a well-posed
task for an agent, we should prefer worlds where the correspondence limit is a
literal, checkable numerical/scale limit (as in EFT and Israeli-Goldenfeld),
not a philosophically contested one.

### 4. Computational mechanics / epsilon-machines (Crutchfield and collaborators).
- URLs: https://link.springer.com/article/10.1023/A:1010388907793 (Shalizi &
  Crutchfield, "Computational Mechanics: Pattern and Prediction, Structure and
  Simplicity"); https://www.quantamagazine.org/the-new-math-of-how-large-scale-order-emerges-20240610/

**What it says.** Computational mechanics defines a process's minimal sufficient
statistic for prediction — the causal states — and the epsilon-machine is the
unique minimal, maximally predictive representation built from those states. Its
statistical complexity (size/entropy of the causal-state machine) is a
scale-dependent, well-defined number: coarse-graining or looking at a process at
different resolutions/timescales generally changes the induced epsilon-machine,
sometimes drastically simplifying it (an "emergent" simple machine at one scale
from a complex generator at another).

**Why it matters / caveat.** This gives us a *measurable, generator-agnostic*
notion of "how simple is the best possible law at this scale," independent of
committing to a particular hand-picked coarse variable. It's a good candidate
metric for automatically verifying, in a generated world, that regime A really
does have a low-complexity epsilon-machine (a "shallow" law is learnable cheaply)
while regime B's best epsilon-machine is much larger (no shortcut without the
deeper theory). I did not find (in the search budget available) a specific
paper applying epsilon-machines directly to a multi-regime/depth-knob generator;
this is my inference of an application, not a claim from the sources.

### 5. Wolfram: computational irreducibility and "pockets of reducibility."
- URLs: https://en.wikipedia.org/wiki/Computational_irreducibility ;
  https://www.stephenwolfram.com/questions/2011/11/03/computational-irreducibility-is-like-prime-numbers-in-a-sense-right-so-as-long-as-it-has-pockets-of-reducibility-it-is-not-the-fundamentally-irreducible-thing-its-not-the-universe-thats-comput/

**What it says.** Wolfram's claim: even inside an overall computationally
irreducible system there exist infinitely many "pockets of computational
reducibility" — sub-questions or sub-observables about which you can say
something with much less computation than full simulation. Ordinary science, in
this framing, is exactly the activity of finding and exploiting such pockets;
computational irreducibility is what limits science and produces "surprises."
**Flag: unverifiable/underspecified.** The Wikipedia article explicitly states
that *no general structural criterion* is known for which systems/observables
admit such pockets — "It is unknown what conditions would allow complex
phenomena to be described simply and predictably" is presented as an open
question, not solved by Wolfram's writing. Israeli & Goldenfeld's paper is the
much more concrete, mechanistic answer to this open question (see #1): the
existence of a pocket of reducibility for a *given* observable is decided by
whether the self-consistency condition holds for some (block size, projection)
pair.

### 6. 't Hooft, cellular automaton interpretation of quantum mechanics.
- URL: https://link.springer.com/book/10.1007/978-3-319-41285-6 (book); overview
  via search results only, not fetched in full.

**What it says (as summarized by secondary sources; I did not read the primary
text in depth given time budget).** 't Hooft proposes that quantum mechanics is
an effective, statistical description of an underlying deterministic
discrete/cellular-automaton-like microscopic dynamics; QM's apparent randomness
and operator formalism are argued to emerge from information loss
(coarse-graining, dissipation into a "class" of the automaton's states) at the
level accessible to observers, while the "hidden" fine-grained dynamics remains
deterministic. **Flag:** this is a speculative, non-mainstream physical model,
not an established result like EFT/RG — I'm including it because it is a
prominent example, at the scale of actual fundamental physics, of "layered
determinism": a deterministic discrete substrate whose effective, empirically
accessible layer is a different (probabilistic-looking) theory. I could not
independently verify the technical claim (only summaries), so treat this as
weak/illustrative evidence, not load-bearing.

### 7. Lakatos / Kuhn — structural conditions for anomalies and degenerating
programmes.
- URL: https://plato.stanford.edu/entries/lakatos/ ; https://link.springer.com/article/10.1007/s13194-025-00677-x (search summary only, not fetched in full)

**What it says.** Lakatos's structural criterion: a research programme is
progressive if successive theory-versions have excess empirical content over
their predecessor *and* some of that excess is corroborated; it is degenerating
if changes are ad hoc patches added only to accommodate anomalies after the fact,
with no novel predictions. Every programme carries "unsolved problems and
undigested anomalies" at all times — anomalies alone don't refute a programme;
what matters structurally is whether the response to an anomaly is
progressive (predicts new facts) or degenerating (just absorbs the anomaly).

**Why it matters / caution.** This is the least directly applicable of the
sources to *generator design* (it's about scientist behavior/theory dynamics,
not world structure), but it does hand us a design criterion for grading agent
behavior once an anomaly is found: a good agent response to a broken shallow law
should be theoretically progressive — the revised/deeper law should predict
new, checkable phenomena beyond just patching the one observed failure, and we
could grade "investigate, revise" episodes partly by this Lakatos-style
progressive/degenerating distinction rather than just correctness-on-the-anomaly.

## Synthesis: what structural feature controls the crossover?

Across the concrete, verifiable sources (Israeli-Goldenfeld; EFT/RG), the answer
is convergent and mechanical, not just an analogy:

1. There must be a genuine **separation of scales** in the world's construction —
   some quantity (spatial block size, energy/speed, time horizon, density) along
   which the world's behavior can be *coarse-grained* at all.
2. A "shallow law" exists at a given scale exactly when a **self-consistency /
   commutation condition** holds: coarse-graining the fine dynamics and evolving
   under the fine rule commutes with evolving under some simpler coarse rule.
   This is a checkable, binary, per-scale fact (Israeli-Goldenfeld's Eq. 3), not
   a vague notion of "roughly similar."
3. That condition is **generically scale- and observable-dependent**: it can hold
   for one projection/blocking and fail for another, and it can hold up to a
   threshold in the scale parameter and fail beyond it (EFT: below cutoff Λ it
   holds to good approximation, at/above Λ the neglected operators are no longer
   small).
4. The **small parameter controlling validity** is always a ratio: (probe
   scale)/(cutoff scale) — concretely instantiated as block size N (spatial
   coarse-graining), energy/Λ (EFT), or n → ∞ (Bohr correspondence, though this
   one is philosophically messier per SEP's caveat).
5. When you push the probe/intervention past the cutoff — go finer, go faster, go
   further out of the training range — the self-consistency condition stops
   holding, and the shallow law's predictions diverge from the fine truth in a
   structured, non-arbitrary way (it doesn't just "become wrong," it fails via
   specific new terms/behaviors becoming visible, which is what makes "revise"
   possible rather than "throw out and restart").

## 5 concrete world-design ideas, each traceable to a source

1. **Blocked/projected cellular automaton with explicit self-consistency
   breakdown.** Build the world as an ECA (or a richer multi-symbol CA), and
   choose in advance a fine rule and a family of (block size N, projection P)
   pairs such that self-consistency (Israeli-Goldenfeld Eq. 3) holds exactly for
   N ≤ N* under projection P, and provably fails for N > N*. Agents observing at
   coarse resolution N ≤ N* see a simple deterministic update rule; if they
   "zoom in" (reduce their observation block size / increase resolution of their
   probes) past N*, the simple rule starts producing wrong predictions and the
   true fine rule must be discovered. Depth knob = N* (how far you can coarsen
   before consistency breaks) and choice of P. Traceable to: Israeli & Goldenfeld
   2006 / arXiv:nlin/0309047.

2. **Cutoff/scale-ratio design using an explicit "speed" or "density" parameter.**
   Give the world a built-in maximum propagation speed or density-dependent
   interaction rule (light-cone-like CA, or particle-density CA à la lattice
   gases). Define the shallow law as the low-speed/low-density limit (where
   interactions are effectively independent/linear) and require it to break down
   as an agent's intervention density or requested propagation speed approaches
   the built-in cutoff — directly mirroring EFT's (E/Λ) expansion parameter. The
   agent discovers the cutoff by pushing interventions faster/denser until
   residuals appear. Traceable to: EFT/RG literature (arXiv:2507.17573;
   Synthese "renormalisation group and effective field theories").

3. **Correspondence-checked hierarchy of rules, not just a broken rule.**
   Require by construction that the deeper (fine) rule, restricted to the
   validity regime of the shallow rule, reproduces the shallow rule's predictions
   either exactly (in the CA/RG case) or within a stated small residual —
   explicitly building in the correspondence principle rather than having two
   unrelated hand-authored rules stapled together. This avoids the SEP-flagged
   failure mode of correspondence relations that are only superficial. Traceable
   to: Bohr correspondence (SEP) + Israeli-Goldenfeld's partial-order/hierarchy
   result.

4. **Grade "depth" by epsilon-machine statistical complexity, not by rule
   author's intuition.** Instead of hand-labeling "regime A is simple, regime B
   is hard," compute (or approximate) the causal-state/epsilon-machine
   complexity of the coarse observable time series in each regime. Use this as
   an automatic, objective knob/metric for how much "depth" a given regime
   requires and to grade agent-submitted programs by how well they match the
   minimal predictive machine, not just point-prediction accuracy. Traceable to:
   Shalizi & Crutchfield, computational mechanics.

5. **Multiple simultaneous projections with different breakdown points (a
   genuine "layers" world, not just two levels).** Following the observation
   that Israeli-Goldenfeld's reductions form a partial order over block sizes,
   construct a world with several nested projections P1 ⊂ P2 ⊂ ... each valid up
   to its own N*, giving more than one reachable anomaly and more than one
   "deeper" layer — Newtonian, then relativistic, then whatever's next — rather
   than a single fit/fail/done arc. This directly supports the brief's "sequence:
   fit, fail, investigate, revise" as a repeatable loop rather than a one-shot
   twist. Traceable to: Israeli-Goldenfeld's partial-order-of-reductions result;
   generalized structurally by the EFT tower-of-scales picture.

## Strongest objections / warnings raised by the literature

- **No general criterion for when reducibility exists.** Wolfram/Wikipedia
  explicitly says it's an *open question* which systems/observables admit
  pockets of reducibility at all — Israeli-Goldenfeld is a worked existence
  proof for specific ECAs, not a generative theory that tells you, for an
  arbitrary rule you might design, whether a nice depth-knob will exist. Design
  risk: a generator built "by hand" to look CA-like may simply not have any
  clean coarse-graining, and you may not know in advance without testing (per
  their paper, some rules — 30, 45, 106 — resisted their own coarse-graining
  search).
- **Correspondence limits can be qualitative, not just quantitative.** SEP's
  discussion of Bohr correspondence's photon/wave mismatch warns that "reduces
  to the old theory in a limit" can be philosophically and technically messier
  than a clean small-parameter expansion; if our generator's correspondence
  isn't literally exact/near-exact and checkable, we risk building something
  that looks like layered physics but isn't actually a well-posed reduction —
  undermining the ability to grade "revise" objectively.
  a rule to reproduce it "for free" only in the trivial region and
  qualitatively differently elsewhere, which is hard to distinguish from just
  having two unrelated rules.
- **Computational irreducibility at the microscopic level is compatible with,
  not opposed to, an exact macroscopic law** — but only for the *chosen*
  observable/projection. This means "depth" is not an intrinsic property of a
  world but a property of (world, observable). Any benchmark claim like "this
  world has depth D" needs to specify which observable/probe the agent is
  allowed, since the same generator could look shallow-and-clean under one
  choice of measurement and multi-layered under another (Israeli-Goldenfeld's
  own point about eliminating "redundant" vs. "relevant" degrees of freedom).
- **Lakatos/Kuhn caution:** anomalies are omnipresent in any real research
  programme and don't by themselves force revision; if the benchmark's grading
  simply rewards "found an anomaly, patched the rule," it risks rewarding
  degenerating, ad hoc fixes rather than genuinely progressive
  theory-replacement — the grading design should check that the revised
  submitted program predicts more than just the one observed anomalous
  instance.
