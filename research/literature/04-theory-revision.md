# Theory revision: cognitive science and ML-theory angle

Angle: what makes a task genuinely require REVISING a theory (not selecting from
a fixed menu), what environmental conditions let an agent (human or LLM) notice
an anomaly and recover, and what current evidence says LLMs fail at here.

Rule followed: every claim below is tied to a source I actually opened via
WebSearch (I did not have live WebFetch page-rendering beyond search snippets
for all of these — where I'm relying on search-result summaries rather than
the full PDF text, I flag it as "per search summary, not independently
verified against full text"). Inferences of mine are marked "MY INFERENCE."

## 1. Bayesian program induction / theory learning (the LOT tradition)

**Ullman, Goodman & Tenenbaum, "Theory learning as stochastic search in the
language of thought," Cognitive Development 27(4), 2012.**
https://www.sciencedirect.com/science/article/abs/pii/S0885201412000445
(also MIT DSpace: https://dspace.mit.edu/handle/1721.1/102507)
Per search summary: theories are represented as sets of logical laws generated
by a probabilistic context-free grammar (a "language of thought"), and theory
learning is stochastic search at two nested levels — an outer loop searching
the space of *theories* (grammar-generated law-sets) and an inner loop
searching the space of *models/explanations* given a fixed theory. Why it
matters for us: this two-level search is close to a formal spec of what our
benchmark should force an agent to do — fit within a theory (inner loop, cheap)
until inner-loop fit degrades enough that outer-loop theory-search pays off.
The paper argues this structure is what lets *qualitative, discontinuous*
theory change look like search rather than gradient descent — directly
relevant to why our worlds should have discrete "regime" structure rather than
smooth parameter drift.

**Kevin Ellis et al., "DreamCoder: Bootstrapping inductive program synthesis
with wake-sleep library learning," PLDI 2021.**
https://dl.acm.org/doi/10.1145/3453483.3454080 (PDF:
https://www.cs.cornell.edu/~ellisk/documents/dreamcoder_with_supplement.pdf)
Per search summary: alternates a "wake" phase (search for programs solving
tasks using the current library of abstractions) and a "sleep" phase (extract
reusable subexpressions from successful programs, add them to the library if
they shorten description length / MDL). Why it matters: this is a concrete
mechanism for *hypothesis-class growth*, not just within-class search — the
library itself is revised over time as the agent meets harder tasks. MY
INFERENCE: this maps onto our "depth knob" — a shallow library solves the
common regime; a genuinely deeper regime should require synthesizing a new
primitive/abstraction that wasn't expressible before, which is a much stronger
notion of "revision" than reweighting a fixed hypothesis menu.

## 2. Misspecification in statistical/ML learning theory

**General ML-theory search results** (arxiv 2608.13633, 2605.10282, and
related; these are recent/technical arXiv notes rather than one landmark
paper, so treat as a survey of the current framing rather than a single
citable claim) — per search summaries: classical learning theory typically
assumes realizability (the true function lies in the hypothesis class); under
misspecification, an estimator does not simply fail but converges to the
element of the class *closest* (under the loss/scoring rule used) to the true
function. Detecting misspecification is distinguished from outlier detection:
rarity of a data point is not itself evidence the model class is wrong — you
need a systematic pattern of residual structure. Bayesian model averaging is
provably suboptimal under misspecification unless you either (a) score models
by a proper scoring rule robust to misspecification, or (b) leave the class
via "improper learning" (predict from outside the original hypothesis class
entirely).

Why this matters for us: it gives a formal vocabulary for two distinct failure
modes we want our worlds to distinguish — (1) *within-class* error (a
parameter is just wrong, more data / reweighting fixes it — this is NOT
revision, it's fitting) vs. (2) *misspecification* (no parameter setting in
the current hypothesis class explains the anomalous regime — this IS revision,
and requires leaving the class). MY INFERENCE: a benchmark that wants to test
"theory revision" must be built so that regime 2 is unreachable by any amount
of Bayesian updating inside the shallow class — otherwise a sufficiently
patient curve-fitter "solves" it without ever revising, which would falsify
our whole design premise. The generator's "depth knob" should be checked
against this: does the deep regime admit *any* member of the shallow
hypothesis class as an approximately-sufficient fit, even a bad one? If yes,
it's not a revision task, it's a hard-fitting task.

## 3. Intervention-based causal learning in humans

**Steyvers, Tenenbaum, Wagenmakers & Blum, "Inferring causal networks from
observations and interventions," Cognitive Science 27(3), 2003.**
https://onlinelibrary.wiley.com/doi/pdf/10.1207/s15516709cog2703_6 (PDF also
at http://web.mit.edu/cocosci/archive/Papers/steyvers-etal-2003.pdf)
Per search summary: participants could partially distinguish competing causal
hypotheses from pure observation, but performance improved substantially once
they could perform and observe the effects of *interventions* they chose
themselves. Why it matters: baseline evidence that active intervention is not
a cosmetic addition to passive observation but does distinct epistemic work —
supports our "run vs. poke" design (passive runs alone should leave some
worlds underdetermined; interventions should be what breaks the tie).

**Bramley, Lagnado & Speekenbrink, "Conservative forgetful scholars: How
people learn causal structure through sequences of interventions," JEP:LMC
41(3), 2015.**
https://www.bramleylab.ppls.ed.ac.uk/publication/2015-01-01_bramley2015fcs/
(PubMed: https://pubmed.ncbi.nlm.nih.gov/25329086/)
Per search summary: people select interventions to maximize information gain,
but they *forget* much of the evidence from earlier trials, and compensate by
being *conservative* — preferring causal structures consistent with their
previously stated beliefs, i.e., resisting revision even under an
information-maximizing intervention policy. Why it matters: this is direct
cognitive-science evidence for a "sticky prior" failure mode that we should
expect to see in an artificial agent too, and it suggests the benchmark should
score not just whether the correct theory is eventually found, but whether the
agent's stated theory tracks the evidence it has already collected (an
"internal consistency"/conservatism metric), because humans (and by extension,
naive agents) can accumulate disconfirming evidence and still fail to update
their explicit theory.

**Coenen, Rehder & Gureckis, "Strategies to intervene on causal systems are
adaptively selected," Cognitive Psychology, 2015** (search results surfaced
this under "Coenen 2015"; I was not able to independently open the full text,
only see it cited as a foundational active-intervention-selection paper
alongside Steyvers 2003 and Bramley 2015 in subsequent literature, e.g. the
MIT active-learning review at
https://link.springer.com/article/10.1007/s42113-023-00195-0). Flag: could not
verify claims directly against primary text — treat title/authorship as
confirmed, content characterization as secondhand.

**Gong, Bramley et al., continuous-time active causal structure learning
(ScienceDirect 2022/2023, "Active causal structure learning in continuous
time," and the 2023 "Show and tell" and related continuous-time causal
induction papers).**
https://www.sciencedirect.com/science/article/pii/S0010028522000780 and
https://www.sciencedirect.com/science/article/pii/S0010027723001646
Per search summary: extends the discrete-intervention paradigm to continuous
time and to abstract "generative/preventative/non-causal" three-component
devices, studying when and where people choose to intervene when interventions
are part of an ongoing stream rather than discrete probe/respond trials. Why
it matters: our simulated worlds are meant to run continuously and be
"poked" — this literature is the closest cognitive-science analogue to what
an agent does when it can both let a world run and intervene mid-run, and
supports building worlds where *timing* of intervention (not just which
variable) carries information.

## 4. Children/adults as "intuitive scientists" — anomaly detection and recovery

**Bonawitz et al., "Children balance theories and evidence in exploration,
explanation, and learning," Cognitive Psychology, 2012.**
http://nwkpsych.rutgers.edu/~bonawitz/BonawitzetalBalance12.pdf
Per search summary: 6- and 7-year-olds revise their predictions after
theory-violating evidence much more readily when that evidence *cannot be
easily explained away* by an auxiliary variable, than when it can. If a
child's exploration turns up a plausible confound, they keep the old theory
and attribute the anomaly to the confound; only when exploration fails to find
an escape hatch do they actually update the theory itself.

Why this matters — this is arguably the single most load-bearing finding for
our design: **an anomaly only forces revision if the environment does not
offer a cheap, available auxiliary-variable excuse.** If our generated worlds
let the agent explain away the deep-regime anomaly by blaming noise, a
uncontrolled nuisance parameter, or measurement error, agents (and possibly
grading) will never be forced into real revision — they'll patch a fudge
factor instead. The anomaly-inducing regime needs to be exploration-hardened:
the agent must be able to *rule out* auxiliary explanations by intervention
(e.g., hold everything else fixed and the anomaly persists), not just observe
the anomaly once.

Related citations surfaced in the same literature stream (title/venue
confirmed via search, not independently opened): Schulz & Bonawitz 2007 on
recognizing confounded evidence, Schulz & Sommerville 2006 on evidence
pointing to an unknown causal variable, Gweon et al. 2010 on recognizing
inconclusive evidence, and the review "Developing an Understanding of Science"
(Annual Review of Developmental Psychology,
https://www.annualreviews.org/content/journals/10.1146/annurev-devpsych-060320-092346)
and Bonawitz/Gopnik-adjacent Science 2012 review "Scientific Thinking in Young
Children" (https://www.science.org/doi/abs/10.1126/science.1223416) — both
summarizing the broader "intuitive scientist" evidence base. Flag: reviewed at
the search-summary level only, not full text.

## 5. Equation discovery / symbolic regression systems that revise models

**Langley, Bradshaw, Simon & Zytkow, BACON and successors (book: "Scientific
Discovery: Computational Explorations of the Creative Processes," MIT Press,
1987; overview page http://www.isle.org/~langley/discovery.html).**
Per search summary: BACON is data-driven — given a table of measurements it
searches for invariants (ratios/products that stay constant across trials) and
builds up concepts incrementally (e.g., rediscovering specific heat and
Black's law of thermal equilibrium from temperature-mixing data). Historically
positioned as automating "data-driven" discovery, contrasted with
"theory-driven" discovery, and later work (BACON.5, and the reconciling paper
at https://ai-2-ase.github.io/papers/14_AAAI_BACON_camera_ready.pdf) explicitly
revisits BACON to compare classical symbolic-search discovery with modern ML.
Why it matters: BACON's mechanism (introduce a new derived quantity/concept
when raw variables don't yield an invariant) is a very old, very literal
example of "grow the hypothesis space when the current one won't fit" — a
minimal existence proof that revision can be implemented as concept
introduction rather than parameter search. MY INFERENCE: our generator's
"depth knob" could literally be: shallow theory = fits with existing variable
set; deep regime = requires a derived/latent variable not observable directly,
forcing something BACON-like (or DreamCoder-like) rather than curve-fitting.

**Udrescu & Tegmark, "AI Feynman: a physics-inspired method for symbolic
regression," Science Advances 2020.** https://arxiv.org/abs/1905.11481,
https://www.science.org/doi/10.1126/sciadv.aay2631
Per search summary: recursively decomposes symbolic regression using
physics-inspired priors — dimensional analysis, symmetry detection (via a
fitted neural net), separability — and this decomposition is precisely what
lets it succeed where generic regression fails (rediscovers 100/100 Feynman
equations vs. 71/100 for prior tools, and 90% vs 15% on a harder set). Why it
matters: AI Feynman still assumes one fixed, "flat" search space of algebraic
expression trees; it does not model regime change (its rediscovered equations
are each valid everywhere, not effective-theory-with-cutoff). MY INFERENCE:
this is a **negative datapoint for our design** — it shows symbolic regression
succeeds by making the flat hypothesis space easier to search, not by handling
nested regimes of validity; none of the classic equation-discovery systems
(BACON, AI Feynman) I found model "this law works until X, then breaks."
That's exactly the gap our benchmark should be targeting, and it means we
shouldn't expect existing symbolic-regression baselines to have any special
capacity to represent regime boundaries — they'd need to be given regime
membership as an extra output, not just a formula.

**AI-Descartes (Cornelio et al.), "Combining data and theory for derivable
scientific discovery," Nature Communications 2023.**
https://www.nature.com/articles/s41467-023-37236-y,
https://arxiv.org/abs/2109.01634; follow-on: "AI Hilbert" (2023,
https://arxiv.org/pdf/2308.09474) and "The Need for Verification in
AI-Driven Scientific Discovery" (Cornelio, 2025,
https://arxiv.org/pdf/2509.01398).
Per search summary: symbolic regression proposes candidate formulas from data;
a theorem-prover-based reasoning module then checks each candidate against
background axioms/theory, filtering for logical consistency rather than only
fit quality. Why it matters: this is a rare system that treats "is this
hypothesis *consistent* with what we already believe" as a first-class check,
not just goodness-of-fit — closer in spirit to what a scientist does when
deciding whether new data merely extends or actually contradicts a theory. The
2025 "Need for Verification" paper (per search summary) argues explicitly that
current AI-driven discovery pipelines under-verify candidate hypotheses before
treating them as established — relevant warning for how we grade: exact-match
program equivalence in our simulator sidesteps this problem (we don't have to
trust the agent's self-report), but if we ever allow partial credit for
"explanation quality" we'd inherit this verification gap.

## 6. LLMs and hypothesis/belief revision — 2024-2026 evidence

**"Belief Revision: The Adaptability of Large Language Models Reasoning,"
EMNLP 2024.** https://aclanthology.org/2024.emnlp-main.586/
Per search summary: evaluates whether LLMs can appropriately revise
conclusions when new, contradicting information is introduced, across a range
of prompting strategies; finds LLMs generally struggle to revise appropriately
— they either over-anchor on the initial conclusion or over-correct
inconsistently rather than doing principled updating.

**"Are LLM Belief Updates Consistent with Bayes' Theorem?"** (arXiv
2507.17951, https://arxiv.org/pdf/2507.17951) — per search summary, tests
LLM belief updates against the Bayesian normative standard directly; framing
implies systematic deviations are found (title alone confirmed via search
snippet; I did not open full text — flag as unverified in detail).

**"When Should Models Change Their Minds? Contextual Belief Management in
Large Language Models"** (arXiv 2605.30219,
https://arxiv.org/html/2605.30219v1) and **"Large Language Model Reasoning
Failures"** (arXiv 2602.06176, https://arxiv.org/pdf/2602.06176) — per search
summaries, these describe "contextual inertia": models fail to revise earlier
generations/intermediate inferences even after later evidence contradicts
them, and this gets worse in long, multi-turn interactions as models lose
track of or deprioritize the relevant earlier evidence. Also: "When Two LLMs
Debate, Both Think They'll Win" (arXiv 2505.19184,
https://arxiv.org/html/2505.19184v2) — per search summary, LLM debaters
persistently overestimate their own position's likelihood of winning even
after seeing the opposing argument, another angle on failure to downweight a
committed position under counter-evidence. Flag: all four are read at the
search-summary level only; I did not fetch full PDFs, so treat mechanism
details as provisional, but the *convergent theme* across four independent
2024-2026 papers (initial-conclusion anchoring, non-Bayesian updates,
contextual inertia across turns, and debate overconfidence) is fairly load-
bearing as a pattern even without full-text verification of any single one.

Why this matters for us: this is the most direct motivation for the
benchmark's existence — there is now a small but convergent 2024-2026
literature specifically documenting that LLMs (a) anchor on an initial
hypothesis, (b) don't update in a normatively correct (Bayesian) way even when
they do update, and (c) lose track of disconfirming evidence over long
interactions. Our benchmark's "run, poke, submit a program" loop is long and
multi-turn by construction (exactly the setting where "contextual inertia" is
reported), so it should be a discriminating test of exactly this weakness —
but only if the world is built so revision is *actually required* (see §2's
warning) and so the anomaly can't be excused away (see §4's warning).

## Answer to the key question

**What must a task have to require genuine theory REVISION, not menu
selection?**
1. A hypothesis-class boundary that is real, not just a parameter extreme:
   there must exist no member of the shallow/default hypothesis class,
   however tuned, that adequately fits the deep-regime data (ML-misspecification
   literature, §2). If the shallow class can be stretched to fit, agents will
   fit rather than revise, and grading them as "having revised" would be false.
2. The anomaly must be intervention-hardened against auxiliary-variable
   explanations: passive observation of an anomaly is not enough, because both
   children (Bonawitz et al., §4) and, per Bramley 2015 (§3), adults will
   default to blaming a confound or forgetting/discounting the disconfirming
   trial rather than revising, unless the agent can actively rule out
   alternative explanations via its own interventions.
3. Revision should require *introducing new structure* (a new primitive,
   variable, or derived quantity), not just reweighting existing terms —
   otherwise "revision" collapses into ordinary re-fitting (DreamCoder's
   library growth, BACON's derived-invariant introduction, §1 and §5 both
   demonstrate this pattern as the actual mechanism of qualitative change).
4. The task must be run over a long enough interactive horizon that "contextual
   inertia" (§6) has room to bite — a one-shot fitting problem won't surface
   the anchoring/inertia failures the 2024-2026 LLM literature reports;
   multi-turn run/poke/re-theorize loops will.

**What do humans need in the environment to notice an anomaly and recover?**
Per Bonawitz et al. (§4) and the Steyvers/Bramley/Coenen/Gong active-causal-
learning line (§3): they need (a) the ability to actively intervene, not just
watch (interventions substantially outperform observation for structure
identification — Steyvers 2003), (b) an anomaly that survives their attempts
to explain it away with an available auxiliary variable (Bonawitz et al.,
§4), and (c) enough working access to their own evidence history that
"conservative forgetting" doesn't quietly reinstate the old theory (Bramley
2015, §3) — i.e., some form of persistent memory/record-keeping of past
trials, which for an artificial agent maps onto whether it has (and uses)
scratch/notes across a long episode.

**What do studies say LLMs fail at here?** Per the 2024-2026 cluster in §6:
anchoring on an initial hypothesis and resisting correction even given
contradicting evidence; deviating from normative (Bayesian) belief updates
when they do update; "contextual inertia" — failing to propagate a later
correction back through earlier inferences in long interactions; and
overconfidence in a committed position even when directly confronted with a
competing argument (the LLM-debate finding). None of the four papers found
report a case where the failure is *inability to search* a hypothesis space —
the reported failure is motivational/attentional (over-anchoring, losing
track of evidence), which argues our benchmark should specifically stress
long-horizon evidence tracking and revision under a *held, stated* prior
theory, not just one-shot hypothesis generation.

## 5 concrete world-design ideas (traceable to sources)

1. **Hard hypothesis-class boundary via a derived/latent variable.** Make the
   deep regime require a new derived quantity (a BACON-style invariant, or a
   DreamCoder-style new primitive) that literally cannot be expressed as a
   parameter of the shallow theory's grammar — not just a coefficient at an
   extreme value. Traceable to Ullman/Goodman/Tenenbaum 2012 (§1), DreamCoder
   (§1), BACON (§5), and the misspecification framing in §2. This guarantees
   "improper learning"/class-leaving is required, closing the loophole where
   an agent fits its way out of trouble.

2. **Confound-proof anomalies: require intervention to rule out excuses.**
   Design the deep regime so that a passive log of the anomaly is
   *always* explicable by at least one plausible nuisance variable, and only
   a targeted intervention (holding candidate confounds fixed) eliminates that
   explanation. Traceable to Bonawitz et al. 2012 (§4) and Steyvers et al.
   2003 / Coenen et al. 2015 (§3). This forces "run vs poke" to be
   epistemically necessary, not cosmetic, and creates a natural grading signal:
   did the agent perform the confound-ruling-out intervention before revising?

3. **Give the agent a persistent notebook and penalize/track forgetting.**
   Because Bramley et al. 2015 (§3) shows conservatism-via-forgetting is a
   real human failure mode, and the 2024-2026 LLM literature (§6) reports an
   analogous "contextual inertia," build long episodes (many run/poke cycles)
   and score not just final-program accuracy but whether the agent's stated
   running theory is consistent with its own accumulated observation log —
   this operationalizes "did it actually revise, or did it just forget the
   counter-evidence."

4. **No free excuse for regime transitions — make the cutoff itself
   discoverable, not given.** Since AI Feynman (§5) and AI-Descartes (§5)
   both work over a single flat hypothesis space with no notion of "valid
   until X," design worlds where the regime boundary (the "depth knob"
   threshold) is itself an unlabeled, interventionally-discoverable fact —
   this is the gap in the equation-discovery literature we can exploit as a
   differentiator, since no baseline symbolic-regression tool natively
   represents "this law only holds below threshold T."

5. **Two-level search structure baked into the generator.** Mirror
   Ullman/Goodman/Tenenbaum's two-loop architecture (§1) directly in how we
   generate worlds: an "outer" combinatorial choice of which mechanism-family
   governs the deep regime (drawn from a small fixed grammar we control, so
   grading stays exact) and an "inner" continuous-parameter regime that is
   easy to fit within a family. This gives us a controllable "depth knob" — a
   world can be made deeper by adding another outer-loop branch point (another
   place where the mechanism family itself changes) rather than by making
   inner-loop parameters harder to estimate.

## Strongest objections/warnings the literature raises

- **Fitting can masquerade as revision (§2).** The single sharpest warning:
  if the shallow hypothesis class is expressive enough (or the loss lenient
  enough), an agent will find a within-class fit for the deep regime and
  never actually revise. We must design against this, e.g., by construction
  proving no member of the shallow-class grammar attains near-zero error in
  the deep regime.
- **Auxiliary-variable excuses defeat anomaly-driven revision (§4).**
  Bonawitz et al. is explicit that this is the *default* response to
  theory-violating evidence — a benchmark that presents anomalies passively,
  without an intervention that can conclusively rule out confounds, risks
  measuring nothing but each agent's tolerance for cognitive dissonance, not
  revision competence.
- **Bayesian updating is not automatically "correct" under misspecification
  (§2).** Even a well-behaved Bayesian-style agent is proven suboptimal once
  the true generative process sits outside its hypothesis class — grading
  should not assume that "more principled updating" alone gets an agent to
  the right answer; leaving the class is a qualitatively different act, and
  our grading rubric (exact program match) should reward that directly rather
  than rewarding calibrated uncertainty over the wrong class.
- **Equation-discovery baselines don't model regimes at all (§5).** Neither
  BACON nor AI Feynman nor AI-Descartes, per what I found, represents "valid
  only in region R." If we want the benchmark to be a meaningful test of
  something novel, this is good news (a real gap to target) but also a
  warning: we can't lean on these systems' internals as prior art for how to
  *grade* regime-boundary discovery — that machinery has to be built new.
- **LLM belief-revision failures are reported at the search-summary level
  only for several papers in §6** — I was not able to open full text for
  arXiv 2507.17951, 2605.30219, or 2602.06176. The *direction* of each
  finding is consistent across four independent papers, which is reassuring,
  but exact effect sizes, task setups, and whether these are frontier or
  smaller models should be checked against full text before being cited as
  hard numbers in any benchmark writeup.
- **Coenen 2015 content is secondhand.** I could not open primary text; only
  title, venue, and its role as a frequently-cited foundational
  active-intervention paper were confirmed.
