# What could the contribution actually be?

2026-09-13. Research assessment, not a PRD or implementation plan. [Evidence and repository audit](2026-09-13-certifiable-experiments-evidence.md).

## Current verdict

**The repository has not yet established a novel scientific contribution.** The user's intuition is a plausible research starting point: require evidence that an environment is a valid test of an intended ability before interpreting agent performance. Its broad formulation overlaps with existing research. A useful contribution may still emerge from a concrete certification method or a new empirical finding; naming a certificate and attaching it to another simulator is insufficient.

The historical experiments establish comparisons within their implemented protocols. They do not establish that hidden-dial worlds require scientific reasoning, that the active certificate is sound, or that the proposed tasks challenge Astra/Fable with coding tools. The local audit identifies a specific truth-inclusion gap, reproduced in the companion note. No new target-model evaluation was run.

## 1. Where the idea meets prior work

| Part of the intuition | Closest inspected precedent | What remains to establish |
| --- | --- | --- |
| Characterize an environment before ranking agents | Hernández-Orallo's [environment difficulty and discriminating power](https://riunet.upv.es/server/api/core/bitstreams/d2867ac3-34a9-4598-9f4b-ed091d7241b1/content), including cellular-automaton examples | A more specific, useful certificate than existing task-difficulty analysis. |
| Prove chosen queries are efficient | [Generalized binary search](https://nowak.ece.wisc.edu/GBS_arxiv_v3.pdf) and [problem-dependent active-learning theory](https://arxiv.org/abs/1108.1766) | Something beyond applying known query-complexity results to a finite hypothesis table. |
| Ground a generated environment in an attainable reference solution | [Alchemy](https://arxiv.org/html/2102.02926v3) has a Bayes-optimal ideal observer | Why the proposed certificate gives additional interpretive or practical value. |
| Test iterative hypothesis revision through experiments | [IVRE](https://papers.nips.cc/paper_files/paper/2023/hash/844f722dbbcb27933ff5baf58a1f00c8-Abstract-Datasets_and_Benchmarks.html); [Zendo rule learning](https://arxiv.org/abs/2402.06025) | A failure mode or measurement result those tasks do not already establish. |
| Certify recovered rules while selecting follow-up experiments | [ABLE](https://github.com/phuayj/able) | A distinction from support-conditional uniqueness and active recovery. |

The possible distinction is **certifying a benchmark item's dependency on a specified capability**, before evaluating the target agents. This could be a methodological contribution if it produces a practical audit with demonstrated added value. It is not automatically a new concept: the broader concern is construct validity, discussed explicitly in [Mitchell's evaluation principles](https://doi.org/10.1002/aaai.70061). The claim needs both a prior-art comparison and results.

## 2. Strengthen the intuition by separating three claims

The existing notes compress three different questions into “needs science”:

1. **Do interventions add information unavailable in the initial observations?** Establish distinct observable answers compatible with the passive record and a legal experiment that separates them.
2. **Does choosing experiments help?** Compare a named selection policy against a specified random policy, using the same inference engine and costs.
3. **Does reacting to results help beyond planning all experiments in advance?** Compare adaptive selection with the best nonadaptive design, or a justified bound on it, under the same task assumptions.

The current proposed smart/random ratio addresses question 2. It does not establish question 3. That distinction has an existing formal treatment: the **adaptivity gap** compares optimal adaptive and nonadaptive strategies. [Golovin & Krause, §11](https://arxiv.org/html/1003.3967v5#S11) study it, including a threshold-learning example. Reusing this distinction is a way to refine the intuition without inventing a new theoretical object.

Even question 1 needs careful wording. Several explanations surviving a finite record does not mean passive observation can never distinguish them. And a learner can guess correctly without obtaining new information. A necessity statement must concern a success guarantee across the remaining possibilities, or expected success under a declared prior—not impossibility for every agent on one fixed seed.

This suggests a sharper research question:

> Can we practically audit generated tasks to establish which benefits come from new observations, which from experiment selection, and which from adapting to the results—and does that audit change our interpretation of agent performance?

This is a proposed investigation assembled from the cited approaches. Its answer and novelty are not known yet.

## 3. What a defensible certificate would actually say

For a small, declared hypothesis class and finite experiment catalogue, the comparison can be made concrete. Fix the initial evidence, reply format, query budget, costs, and either a prior or a worst-case success objective. Merge hypotheses only under the stated observable equivalence.

Then establish two sides:

- **Attainability:** exhibit a policy that uses only available evidence and succeeds at the stated cost. The policy cannot choose experiments by inspecting the hidden answer.
- **Exclusion of the claimed shortcut:** bound success for the relevant restricted alternatives. If the claim concerns adaptive revision, the relevant alternative is an optimally chosen fixed experiment set, not just random pokes.

A finite query table turns this into existing experimental-design and decision-tree machinery. That is a strength for verification but a limitation on novelty. If the whole project reduces to constructing that table and invoking known algorithms, the likely contribution is an application or evaluation resource. A stronger methods result would need to show a useful scale, scope, or verification capability not already available from the closest work.

Keep information and computation separate. An agent may reconstruct the hypothesis space with code and use the reference policy. That counts as success. A large random/smart gap cannot certify hardness for a strong coding agent. Conversely, making enumeration prohibitively expensive also raises the cost of generating exact certificates; a short true rule does not establish an affordable route to discovering it.

The term “certificate” must preserve these distinctions:

| Evidence available | Defensible statement |
| --- | --- |
| One true-answer-aware separating experiment | This experiment distinguishes these alternatives. |
| A policy succeeds on all branches of a finite class | This class is identifiable within this protocol and budget. |
| Greedy beats random in repeated trials | This named policy improves over this random distribution. |
| A lower bound excludes all fixed designs at a budget, while an adaptive policy succeeds | Adaptation is necessary for the specified guarantee. |
| Sampled prediction agreement | No counterexample occurred in these samples. |

None of these alone establishes internal understanding or general scientific intelligence.

## 4. Three possible contributions, with evidence that would earn them

These are alternatives for research focus, not three projects to build.

### A. A practical benchmark-validation method — strongest fit to the intuition

Provide a reusable audit that distinguishes the claims above and exposes shortcuts before a task enters an evaluation. Demonstrate that its findings are more informative than ordinary solve rates and random-baseline gaps.

The smallest informative study is a sound audit of the existing world family, with matched protocol variants: passive information, fixed experiments, adaptive experiments, and richer replies. Include easy and inseparable controls. Freeze the audit rules before looking at target-agent scores. If a second task is needed to establish reuse, apply the audit to an existing symbolic environment instead of inventing another substrate.

**What would make this more than good engineering:** a validated method that changes which items qualify, which capability claims survive, or how agent failures are explained, beyond what the closest methods already reveal. Benchmark-dependent conclusions are a documented concern in [The Benchmark Lottery](https://arxiv.org/abs/2107.07002), but that concern itself is not the contribution.

**What would rule this direction out:** standard version-space analysis already supplies the entire audit, certification is affordable only for trivial toy cases, or audit labels provide no additional explanatory value.

### B. A new empirical finding about scientific agents

Use certified tasks to locate a reproducible limitation: agents may be able to simulate candidates but fail to choose distinguishing experiments, or choose informative experiments but fail to revise the model. These are hypotheses to test, not conclusions from the current pilots.

Compare the same agent with candidates supplied versus inferred, and with experiment choice delegated versus retained. Keep its coding tools, inference budget, and observations explicit. Human studies support treating information selection and processing demands separately; the companion note triangulates this through Steyvers, Coenen, and Gong. They do not predict the result here.

**What would make this a contribution:** a robust, controlled finding about the evaluated agents that survives strong scripted baselines, fresh worlds, and changes that remove transcription burden. Low aggregate success alone is insufficient.

**What would rule it out:** the gap disappears with ordinary code access, prompt/interface repairs, or a matched computational budget. That would still be useful diagnostic evidence, but not the proposed scientific-reasoning limitation.

### C. A theoretical result about tractable certification — highest burden

Investigate whether the existing partially observed dynamics admit a useful certificate whose construction or checking is substantially more tractable than generic exhaustive analysis, with clearly delimited guarantees.

This requires a precise new theorem or algorithm and a comparison against existing learning and planning results. At present there is no such theorem in this repository. “Hidden variables,” “compressed model,” and “proof attached to a seed” do not supply one. [Generalized binary search](https://nowak.ece.wisc.edu/GBS_arxiv_v3.pdf) already makes query-space structure central to guarantees.

This direction should follow a concrete obstruction uncovered by the small audit. It should not be selected just because theoretical novelty sounds stronger.

## 5. What to keep and cut while deciding

Keep the user's demand that the environment justify the inference made from an agent's score. Keep the simulator only as a tractable test case. Keep the distinction between a task being unsolved, being solvable, and requiring a particular source of information.

Temporarily cut the eight-task ranking, new dial mechanisms, leaderboard positioning, and the requirement that the next design defeat specific model names. The “hard for Astra/Fable” goal can remain an empirical challenge criterion after validity is established; it cannot define what counts as scientific reasoning.

Start with one question the current implementation cannot answer soundly: **after correcting the candidate set, is there a meaningful gap between the strongest fixed experimental design and a policy that adapts to replies?** A finite, bounded version is enough to learn whether the intuition needs adaptation, merely better query selection, or a different target capability. Do not generalize from a sampled candidate panel to all theories in the grammar.

If that gap is absent, the active-revision claim fails for that setting. If it exists but a simple script solves every instance, the environment is a useful controlled instrument but may be a weak frontier-agent challenge. If it exists, is practically certifiable, and predicts a stable failure in capable agents, there is a much stronger basis for a research contribution. Each is an informative outcome; none has been established here yet.

## Verification boundary

The novelty assessment compared independent theory, benchmark, and certified-recovery research, and was widened to earlier environment-difficulty work. It establishes overlap, not an exhaustive proof of nonexistence. Human grounding comes from three separate published studies, not three mirrors of one paper. New performance, exact-certification feasibility, and novelty of a future method remain unverified. No PRD, new benchmark implementation, or paid model run was produced.
