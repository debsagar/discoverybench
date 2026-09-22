# Context for literature agents, round 2 (2026-09-22)

We are designing a benchmark (paper is evaluation-only, but we design it as if it were an RL environment so it can be ported later). An AI agent enters an unknown simulated world, can RUN (set initial state, watch), POKE (pause, edit cells, continue; hidden state carried), and SUBMIT a program that simulates the world. We own the simulator, so grading is exact: the program must match the truth frame by frame on held-out situations including interventions. Headline score: percent of worlds solved. Second: recovery after a failed submit.

The chosen substrate: a lattice gas of BALLS ON A GRID. Each cell holds up to four balls (one per direction). Balls move one step per tick. Exactly-two head-on balls in a cell leave sideways (HPP-style collision). Ball count and momentum are conserved.

Planned LAYERS (the depth knob):
- Floor 1: sparse regime, "balls fly straight" fits.
- Floor 2: crowded regime, collision rule needed.
- Floor 3: each ball carries a hidden inner state that flips on certain collisions and changes later collisions; only detectable by designed crashes.
Rules: each deeper floor must reduce to the floor above in calm conditions, be reachable by poking within budget, and not be fixable by fudging the shallower theory.

Rules for you:
- Use WebSearch and WebFetch. Do NOT answer from memory. Every claim needs a source you actually opened, with URL. Prefer primary papers.
- Separate "what the source says" from "my inference". Flag anything unverified.
- Plain language, no hype. End with concrete design recommendations traceable to sources, plus the strongest warnings.
