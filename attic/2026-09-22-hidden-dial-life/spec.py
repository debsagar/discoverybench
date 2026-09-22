"""Module 1: world specification.

A world is a 2-D toroidal grid. Each cell carries two values:

  v - visible state, binary {0,1}. The only thing an agent will ever see.
  h - hidden state, in {0..H-1}. Never shown to anyone but the simulator.

Dynamics, per step (all cells update simultaneously from the previous frame):

  count = number of live visible neighbors (Moore 8-neighborhood, torus)
  v'    = birth[h][count]   if v == 0
        = survive[h][count] if v == 1
  h'    = h_next[h][d]      d = driver signal, see drivers.py (the twist)

So each hidden state selects a different Life-like rule table, and the hidden
state is a small deterministic machine fed by a binary signal. Because v'
depends on h, and h encodes the past, the visible process alone is
non-Markovian: two identical visible frames can evolve differently.

The spec IS the world: same spec + same initial state => same rollout forever
(for h0 == "random" the initial hidden field is drawn by the caller's rng).
"""
from dataclasses import dataclass, field

import numpy as np

# name -> (driver, h0 mode). Params (tau, T) are sampled per world.
TWISTS = {"own": ("own", "zero"), "count": ("count", "zero"), "clock": ("clock", "zero"),
          "own_h0": ("own", "random"), "count_h0": ("count", "random")}


@dataclass(frozen=True)
class WorldSpec:
    birth: np.ndarray    # bool, shape (H, 9): birth[h][count]
    survive: np.ndarray  # bool, shape (H, 9): survive[h][count]
    h_next: np.ndarray   # int,  shape (H, 2): h_next[h][d]
    seed: int = field(default=-1)
    driver: str = "own"
    param: int = 0       # tau for count, T for clock
    h0: str = "zero"     # "zero" | "random"

    @property
    def n_hidden(self) -> int:
        return self.birth.shape[0]

    @property
    def twist(self) -> str:
        return next(k for k, v in TWISTS.items() if v == (self.driver, self.h0))

    def describe(self) -> str:
        lines = [f"WorldSpec(seed={self.seed}, H={self.n_hidden}, twist={self.twist}, param={self.param})"]
        for hs in range(self.n_hidden):
            b = "".join(str(c) for c in range(9) if self.birth[hs][c])
            s = "".join(str(c) for c in range(9) if self.survive[hs][c])
            lines.append(f"  h={hs}: B{b}/S{s}   h_next(d=0)->{self.h_next[hs][0]}  h_next(d=1)->{self.h_next[hs][1]}")
        return "\n".join(lines)


def _param(rng, driver):
    return {"own": 0, "count": int(rng.integers(1, 9)), "clock": int(rng.integers(2, 9))}[driver]


def sample_spec(seed: int, n_hidden: int = 3, twist: str = "own",
                p_birth: float = 0.25, p_survive: float = 0.5) -> WorldSpec:
    """Sample a random world. Deterministic in (seed, n_hidden, twist).

    p_birth/p_survive are inclusion probabilities per neighbor count, tuned so
    a decent fraction of sampled worlds stay active (the rest get filtered
    empirically by certification, not here).
    """
    driver, h0 = TWISTS[twist]
    # ponytail: baseline keeps the legacy stream so seeds 21, 12, ... still name the Phase 0 / pilot worlds
    rng = np.random.default_rng(seed if twist == "own" else [seed, list(TWISTS).index(twist)])
    ident = np.arange(n_hidden)
    while True:
        birth = rng.random((n_hidden, 9)) < p_birth
        survive = rng.random((n_hidden, 9)) < p_survive
        h_next = rng.integers(0, n_hidden, size=(n_hidden, 2))
        if driver == "clock":
            h_next[:, 0] = ident          # a clock HOLDS between ticks
        # Light structural sanity only; certification is the real judge.
        rules_differ = n_hidden == 1 or not all(
            np.array_equal(birth[0], birth[hs]) and np.array_equal(survive[0], survive[hs])
            for hs in range(1, n_hidden))
        h_moves = n_hidden == 1 or np.any(h_next != ident[:, None])
        if rules_differ and h_moves:
            return WorldSpec(birth=birth, survive=survive, h_next=h_next, seed=seed,
                             driver=driver, param=_param(rng, driver), h0=h0)
