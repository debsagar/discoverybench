# Certifiable experiments: evidence, novelty, and theoretical limits

Research date: 2026-09-13. Research note for discussing the contribution; the user explicitly dropped the PRD request during this review. No implementation commitment is implied.

Start with the shorter [contribution assessment](2026-09-13-contribution-assessment.md). This file preserves the evidence and technical audit.

## 1. What belongs to the idea, and what the literature already owns

Per the user's attribution, the originating intuition is **environment certifiability**: establish that a generated world rewards a particular kind of reasoning before using it to assess an agent. The hidden-dial implementation and hard-Life task proposals are prior model work, open to replacement. This is attribution within this project, not a claim of priority over the literature.

The project log records the intuition on September 1 as “priced out and compressible,” then reframes it on September 2 around passive ambiguity and deliberate versus random interventions. The latest formulation is the relevant one. A large lookup table losing to a compact model establishes a result against that lookup-table family; it does not establish that experimentation is necessary.

**Novelty verdict: the broad claim is already substantially covered. The narrower benchmark contribution is a candidate, not an established first.** Three distinct lines of prior work constrain it:

| Prior-art check | What is already established | Consequence for this project |
| --- | --- | --- |
| Learning theory | Generalized binary search gives conditions on a hypothesis/query space for efficient identification. Active-learning theory characterizes problem-dependent advantages over passive learning. [Nowak](https://nowak.ece.wisc.edu/GBS_arxiv_v3.pdf), [Hanneke](https://arxiv.org/abs/1108.1766), [Wang](https://jmlr.org/papers/v12/wang11b.html). | “The problem itself can admit a provable advantage from chosen queries” is not new. |
| Interactive benchmarks | IVRE includes ambiguous initial evidence, budgeted experiments, symbolic search baselines, and human evaluation. Alchemy provides procedurally resampled latent structure. DiscoveryWorld evaluates scientific discovery cycles. [IVRE](https://papers.nips.cc/paper_files/paper/2023/hash/844f722dbbcb27933ff5baf58a1f00c8-Abstract-Datasets_and_Benchmarks.html), [Alchemy](https://arxiv.org/abs/2102.02926), [DiscoveryWorld](https://arxiv.org/abs/2406.06769). | Neither generated hidden worlds nor observe–hypothesize–intervene loops establish novelty. |
| Certified active recovery | ABLE's official implementation describes executable Boolean-rule recovery, symbolic uniqueness checks, and active follow-up queries. Its reproduction guide includes certifiability and adaptivity diagnostics. [Official code](https://github.com/phuayj/able), [reproduction guide](https://raw.githubusercontent.com/phuayj/able/master/docs/REPRODUCE.md). | Even “active learning plus rule certificates” is insufficient as a novelty claim. |

Follow-up checks narrow the novelty further. Hernández-Orallo's [On environment difficulty and discriminating power](https://riunet.upv.es/server/api/core/bitstreams/d2867ac3-34a9-4598-9f4b-ed091d7241b1/content) characterizes task instances through populations of policies, including elementary cellular-automaton examples. [Alchemy's ideal observer](https://arxiv.org/html/2102.02926v3) is already a normative reference for a structured, procedurally generated environment. [Golovin & Krause, §11](https://arxiv.org/html/1003.3967v5#S11) explicitly study adaptivity gaps, including an active-learning example. Thus environment-level difficulty, normative solvability, and the value of adaptation are individually prior art too.

The ABLE PDF was browser-challenged, so the detailed comparison relies on its inspected official code. Its [adaptivity experiment](https://raw.githubusercontent.com/phuayj/able/master/src/able/cli/eval_adaptivity_collapse.py) compares no-follow-up and targeted-follow-up configurations; these also differ in candidate-count settings. That code alone does not establish a comparison against the optimal nonadaptive query policy with identical inference. Its [certificate implementation](https://raw.githubusercontent.com/phuayj/able/master/src/able/lift_cert.py) explicitly represents unseen truth-table entries and enumerates their completions. This is directly relevant to the local fitter gap. These are source inspections, not reproduced ABLE results.

[NewtonBench](https://arxiv.org/abs/2510.07172) adds another overlap: interactive discovery of systematically altered physical laws. Separately, [DiscoveryBench](https://arxiv.org/abs/2407.01725) already names an external data-driven discovery benchmark; a future public release should avoid implying this local repository is that project. These checks do not change the present task into a renaming exercise.

The contribution worth testing is more specific: **a benchmark admission procedure that ships each generated instance with reproducible evidence of initial ambiguity, accessible discriminating experiments, and a measured advantage over named alternative query policies under the same interface.** A further empirical contribution would be showing where capable coding agents fail despite that attainable reference performance.

These reviewed sources do not establish an exact match to that complete admission procedure. That is a bounded search finding, not evidence that no match exists. Before a publication claim, inspect the closest implementations against the actual certificate fields and attempt the same audit on IVRE or ABLE. A change of substrate alone is not a sufficient difference. No new theorem or algorithm is claimed here.

## 2. Human evidence: what is actually grounded

Three independent human studies support the general choice to study intervention selection. They do not test this cellular automaton or establish difficulty for today's target models.

| Study | Human evidence inspected | What it supports; what it does not |
| --- | --- | --- |
| Steyvers et al., 2003 | The original publication reports three causal-inference tasks and improved performance when participants could intervene. [Paper](https://onlinelibrary.wiley.com/doi/10.1207/s15516709cog2703_6). | Supports comparing observation with intervention. Does not establish permanent observational ambiguity in these Life worlds. |
| Coenen, Rehder & Gureckis, 2015 | Experiment 1 recruited 105 participants, using pairs of candidate causal structures. Reported mean graph-choice accuracy was 87%, with 1.56 interventions per chip test. Later experiments altered incentives and time pressure. [Paper, §§2–4](https://bpb-us-e1.wpmucdn.com/wp.nyu.edu/dist/4/20443/files/2021/01/Coenen-ea-15-CogPsych.pdf). | Supports explicit rivals and costly experiments as a human task, while showing strategy depends on effort and task conditions. These figures are not performance targets for this benchmark. |
| Gong et al., 2023 | Two experiments investigated intervention timing and targeting in continuous-time causal devices. Experiment 1's final connection judgments averaged 62% accuracy; the stated chance level was 25%. The study analyzes both information and evidential complexity. [Paper, §§2, 6](https://cicl.stanford.edu/papers/gong2023active.pdf). | Supports separating informative experiments from evidence that is difficult to process. Does not imply fewer returned cells automatically make a better task. |

Gong et al. also publish participant-data filenames, analysis, and experiment materials. The [data README](https://raw.githubusercontent.com/tianweigong/time_and_intervention/main/data_analysis/Readme.md) identifies `exp1_final.Rda` and `exp2_final.Rda`, and warns that some large simulation prerequisites are absent. This review inspected the paper and public data documentation; it did **not** reanalyze participant-level data. The paper and its repository count as one study, not two independent confirmations.

Two particularly relevant benchmark precedents strengthen the comparison:

- [IVRE's paper](https://papers.nips.cc/paper_files/paper/2023/file/844f722dbbcb27933ff5baf58a1f00c8-Paper-Datasets_and_Benchmarks.pdf), Table 2, reports episode accuracy of 83.80% for Search-Naive, 34.15% for Search-Random, and 98.15% for humans. These are that paper's conditions and systems, not estimates for Astra or Fable. IVRE therefore already makes experiment-policy comparisons relevant to this proposal.
- [Doing Experiments and Revising Rules with Natural Language and Probabilistic Reasoning](https://arxiv.org/abs/2402.06025) combines LLM proposals, probabilistic updating, experiment design, and a human comparison on a Zendo-style task. Open-ended rule language and human comparisons are also existing directions.

## 3. What “triple verified” means here

Repeated websites describing one paper are not independent verification. Nor can three citations verify a newly proposed design, a mathematical claim without its assumptions, or the absence of prior art.

| Claim family | Three independent checks | Status |
| --- | --- | --- |
| Intervention selection is a meaningful human reasoning task | Steyvers 2003; Coenen 2015; Gong 2023 | Triangulated at the construct level. Transfer to hidden-dial CA remains untested. |
| Query efficiency depends on the declared learning problem | Nowak; Hanneke; Wang, linked above | Triangulated theoretical foundation. Their theorems are not automatically theorems about this simulator. |
| Experimental design must be compared against alternatives | [Hauser & Bühlmann](https://arxiv.org/abs/1205.4174); IVRE; Gong 2023 | Independent algorithmic, benchmark, and human-study precedents. No universal numerical advantage established. |
| Evaluation needs explicit protocols and uncertainty | [Machado et al.](https://arxiv.org/abs/1709.06009); [Agarwal et al.](https://proceedings.neurips.cc/paper/2021/hash/f514cec81cb148559cf475e7426eed5e-Abstract.html); [Pineau et al.](https://jmlr.org/papers/v22/20-303.html) | Supports fixed evaluation conditions, repeated runs, and reproducible reporting; proposed sample sizes still need calibration. |
| This exact admission procedure is novel | Theory comparison; interactive-benchmark comparison; certified-recovery comparison | Unresolved. Three searches cannot prove novelty. |
| The proposed tasks are hard for Astra/Fable or learnable by humans | Existing local pilots use other model identifiers; no new target-model or CA human runs | Unverified. Required experiments, not manuscript claims. |

Any design requirements discussed here are proposals. Numbers inherited from the idea artifact are pilot settings, not externally validated standards. Repository facts are verified against local code/results, not made “web-verified” by attaching unrelated citations.

## 4. The theoretical object being certified

Write the test configuration as:

`(world, initial observations, hypothesis class, legal experiments, reply function, query costs, reference inference, selection policies, success criterion)`.

Omitting any of these can change the conclusion. A simulator seed alone has no fixed experimental difficulty. “Random” must specify a distribution; “smart” must name a policy. With those fixed, the measured comparison does not depend on which LLM is later evaluated. It remains relative to the specified policies and inference engine.

### Ambiguity is relative to evidence and an answer

Let `V(D)` be all hypotheses in the declared class that agree exactly with observations `D`. Each legal experiment `e` partitions it by predicted reply `y`. Updating means retaining only hypotheses that predict the reply actually observed. This is the version-space view used by [generalized binary search](https://nowak.ece.wisc.edu/GBS_arxiv_v3.pdf).

Two different parameter arrays need not represent different observable answers. Hidden-state relabelings can describe the same behavior; different machines can also agree on every allowed test. For a finite experiment catalogue, equality of the entire reply vector defines exact **catalogue-relative** equivalence. Agreement on a few sampled rollouts establishes only sampled agreement.

“Several hypotheses fit 16 frames” means finite-data ambiguity. “Even all allowed no-edit observations leave alternatives” is stronger. “Passive observation can never identify the world” requires a theorem about the full observation process and is not supported by these experiments.

### Short answers constrain information, not necessarily reasoning

For a deterministic reply of `R` binary cells, there are at most `2^R` outcomes. A depth-`B` adaptive decision tree therefore has at most `2^(RB)` leaves. Identifying all `K` equally weighted, distinguishable possibilities requires `B >= ceil(log2(K)/R)` in the worst case. This is an elementary counting derivation, not an observed performance result or a sufficient condition for solvability.

Illustration: eight distinguishable candidates and a one-cell reply require at least three queries in the worst case. Three balanced splits achieve that bound only if such legal experiments exist. A lucky branch can terminate earlier. Making replies smaller can also remove all distinguishing experiments.

A headcount over `A` cells has up to `A+1` outcomes, or at most `log2(A+1)` bits. One number is not necessarily less information than one cell. Cancellation can impede identification, but it must be measured under the actual rules and allowed experiments.

### Existence of a good experiment does not establish a good learner

A designer who knows the true world can choose its separating experiment after looking at the answer. That is not a valid agent baseline. [Machine teaching](https://pages.cs.wisc.edu/~jerryzhu/pub/MachineTeachingAAAI15.pdf) explicitly studies a teacher choosing examples with a target and learner in mind; it helps explain this distinction.

A valid reference policy chooses from its current evidence and candidate predictions before seeing the hidden response. A greedy information-gain policy is established practice; it is not generally optimal. [Mussmann & Liang](https://proceedings.mlr.press/v84/mussmann18a.html) study conditions for efficient generalized binary search rather than a universal guarantee.

Also separate query cost from computation. A solver can enumerate short machines and still select excellent experiments. Calling that “not science” would make the benchmark depend on a preferred internal strategy. If a coding agent writes the same solver and succeeds, it passed. A random-query gap does not prove resistance to computational brute force.

### Identification is not universal explanation

A zero-error executable answer on the declared finite tests establishes predictive agreement there. It does not prove recovery of a uniquely true latent representation, behavior on all future histories, scientific creativity, or real-world scientific competence. These stronger claims require stronger tests or proofs. [ABLE](https://github.com/phuayj/able) is an especially relevant reminder that the scope of a uniqueness check must be stated.

## 5. Repository audit and reproducible local evidence

The repository currently contains a seeded simulator, finite machine enumeration with table fitting, historical certification experiments, and a pilot harness. It does not contain the proposed restricted-reply benchmark. Relevant code: [active.py](../../phase0/active.py), [theorist.py](../../phase0/theorist.py), [pilot.py](../../phase0/pilot.py), [run_pilot.py](../../phase0/run_pilot.py).

| Finding | Evidence | Design consequence |
| --- | --- | --- |
| Survivors use more than the passive transcript | `active.survivors(chunks, held)` checks a separate held-out pool with tolerance `1e-4`. | Agent inference must use public evidence only; keep validation data separate. |
| Fitted tables are not a complete version space | `fit_tables` chooses zero for entries with no counts, returning one completed table per machine. | Preserve both allowed values for unobserved entries when claiming completeness. |
| A true machine does not imply its fitted table is true | Reproduction below; saved `active_own.log` seed 34 has `alive: 47` and `block: 47` killed. | Check the entire truth specification survives every valid observation; an empty version space invalidates the certificate. |
| The active-survival test is weaker than its title | `test_true_theory_survives_passive_watching_and_every_poke` checks machine/driver/parameter presence, then separately compares an explicitly constructed truth against itself. | It does not verify that the actual survivor's birth/survival tables survive every poke. |
| Existing executable exam is conditional next-step prediction | `eval_submitted_model` advances hidden state along true visible prefixes, then predicts one next frame. | Add free rollout after an edit for the new task; do not call old results full model recovery. |
| Existing model runs do not establish target difficulty | Stored filenames and `run_pilot.py` name `openai/gpt-5.4` and `google/gemini-2.5-flash`. | Evaluate actual Astra/Fable configurations and report their exact identifiers and tool access. |

Read-only check, run from `wmi/phase0` on the research date:

```python
import numpy as np
from spec import sample_spec
from enumerator import train_pool, held_out
from theorist import fit_tables, held_err
from active import as_spec, outcome, POKES
w = sample_spec(34, 3, "own")
table, err = fit_tables(w.h_next, train_pool(w, w.seed, 64), "own", 0, 3)
truth = np.stack([w.birth, w.survive], 1).astype(np.uint8)
fitted = as_spec("own", 0, w.h_next, table)
print(float(err), int((table != truth).sum()))
print(held_err(w.h_next, table, held_out(w, w.seed), "own", 0))
print({k: bool(np.array_equal(outcome(fitted, *v), outcome(w, *v)))
       for k, v in POKES.items()})
```

Observed: training error `0.0`; `7` fitted entries differ from truth; held error `8.719308035714285e-06`; equality to truth is false for `block`, `sparse`, `dense` and true for `fill`, `clear`. This shows why approximate passive fit is not exact truth inclusion; it does not show every proposed mid-run experiment fails.

Existing suite: `python3 -m pytest test_wmi.py -q` → `23 passed in 58.54s`. Passing these tests does not close the uncovered certificate gap.

The linked Claude artifact was unavailable through the web. A local copy was found and read at `/tmp/claude-1000/-data-discoverybench/2214f615-b4c4-4f7d-9844-2c9ff15e0399/scratchpad/hard-life-tasks.html`. Its seed-specific success claims and “about 100 lines” estimate lack reproduced supporting runs in this review; they remain proposals. Original project history is in `/data/MathBench/PROJECT-LOG.jsonl`.

## 6. How far the project can grow, and what each cut gives up

This is a map of the existing ideas' theoretical obligations, not an expansion backlog.

| Scope | What it would measure | New obligation | Current cut |
| --- | --- | --- | --- |
| Supplied candidates, fixed experiments | Replay correctness and experiment selection | Complete candidate set and exact replies | Use as a diagnostic; it cannot establish hypothesis invention. |
| Hidden candidate set within a public finite rule grammar | Model construction plus adaptive experiment selection | Complete fitting from public evidence; affordable reference solver | Intended core, only for instances where certification finishes. |
| Edits chained through a changing world | Multi-step experiment construction and state tracking | Reachability and separation over whole action histories | Defer; start each experiment from the same saved checkpoint. |
| Unknown initial hidden state | Joint state and rule inference | Account for all compatible hidden-state assignments | Defer; start at known hidden zero. |
| Two ears / moving thresholds | Richer mechanisms and possible composition | Broader hypothesis class, controls proving added capability | Defer; existing one-dial family must first earn its place. |
| Arbitrary executable theories or new scientific substrates | Broader discovery and transfer | New identifiability, verification, and generalization arguments | No present completeness claim; sampled falsification has a different scope. |

The key tradeoff is exactness versus breadth: expanding what an agent may hypothesize also expands what a complete certificate must rule out. The cheapest defensible cut bounds the class and interface while retaining experimental choice. If even that bounded task is solved routinely by target coding agents, the result establishes a limit of this benchmark proposal. It is not grounds to keep adding mechanisms until somebody fails.

Before broadening, discuss three questions: Is the desired contribution a certificate method or an agent challenge? Must the certificate be exact, or is a named empirical comparison enough? Is hidden-class discovery essential, or is efficient discrimination already the intended ability? These are research choices, not settled product requirements.
