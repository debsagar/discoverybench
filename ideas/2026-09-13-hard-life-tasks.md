# Hard Life tasks

The manager wants a benchmark that is hard for Fable and Astra. Not hard because the grid is big, hard because you cannot get the answer without doing science.

Same world as always: a hidden dial in every cell. What changes is how stingy the world is when you ask it something. The strongest model in the room can read a whole grid. It cannot plan a question whose answer fits in one cell.

Eight tasks, ranked, each with a computable truth and a knob:

1. Peephole. Paint a small patch, the world shows one window at one tick. Pick both so the rival stories disagree there.
2. Keep the rivals alive. Here are eight candidate rules and a short record. Which still fit, and which cell and tick kills each of the others.
3. Full loop, stingy world. Watch, then spend a poke budget with tiny replies, then hand in a runnable rule.
4. Headcount. The world only replies with how many cells are on. Rivals that differ cell by cell often agree on the total.
5. Not Life in one small look. It looks like plain Life. Name one pattern, one window, one frame where it is not.
6. Which crowd threshold. Find the crowding number the dial listens to. One miscount and you are off by one.
7. Two ears. Two dials per cell, one listening to itself, one to the crowd. Watching one region fools you in the other.
8. Moving threshold. What counts as crowded depends on the dial.

Build order: one small engine on top of active.py (dedupe rivals, stingy reply, greedy and random pokers), then the cheap graders, then the two new world types last.

Full write-up with ground truth, knobs and smallest experiment per task:
https://claude.ai/code/artifact/8c4be42f-e9c8-4fbe-9f76-e16ec39c4fec
