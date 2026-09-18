# Context for literature agents

We are designing a benchmark where an AI agent enters an unknown simulated world, runs experiments (run, poke/intervene), and submits a program that simulates the world. We own the simulator so grading is exact. Worlds must be discrete, deterministic, cheap, procedurally generated.

The design insight we want grounded in literature: WORLDS NEED LAYERS. A shallow theory should fit a common regime and then fail in a rarer, reachable regime where only a deeper truth works (Newton works until you go fast). Discovery then becomes a sequence: fit, fail, investigate, revise. We want these properties to EMERGE from how the world is built, the way they do in our universe, rather than being bolted on as tricks. Generator needs a "depth" knob.

Question: what kind of world do we need? What world constructions naturally produce nested regimes of validity, effective theories, and reachable anomalies?

Rules for you:
- Use WebSearch and WebFetch. Do NOT answer from memory. Every claim needs a source you actually opened, with URL.
- Prefer primary papers (arXiv, journals). Give title, authors, year, URL, and 2-4 sentences on what it says and why it matters for our question.
- Flag anything you could not verify. Separate "what the paper says" from "my inference".
- End with: 5 concrete world-design ideas implied by this literature, each traceable to sources, and the strongest objections or warnings the literature raises.
- Plain language. No hype.
