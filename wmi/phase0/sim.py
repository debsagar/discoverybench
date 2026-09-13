"""Module 2: the simulator. Owns ground truth.

Pure functions over numpy arrays; fully vectorized; deterministic. A rollout
is (steps+1, n, n) arrays of visible and hidden states — the hidden array
exists so WE can validate and score, it is never handed to an agent.
"""
import numpy as np

from spec import WorldSpec
from drivers import signal, h0_field


def neighbor_counts(v: np.ndarray) -> np.ndarray:
    """Live visible neighbors per cell, Moore 8-neighborhood on a torus."""
    c = np.zeros(v.shape, dtype=np.intp)
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if dy or dx:
                c += np.roll(np.roll(v, dy, axis=0), dx, axis=1)
    return c


def step(spec: WorldSpec, v: np.ndarray, h: np.ndarray, t: int):
    """One synchronous update of the whole grid at time t. Returns (v', h')."""
    count = neighbor_counts(v)
    v2 = np.where(v == 1, spec.survive[h, count], spec.birth[h, count]).astype(np.uint8)
    h2 = spec.h_next[h, signal(spec.driver, spec.param, v, count, t)].astype(np.uint8)
    return v2, h2


def rollout(spec: WorldSpec, v0: np.ndarray, h0: np.ndarray, steps: int):
    """Returns (V, H) with shapes (steps+1, n, n); frame 0 is the initial state."""
    V = np.empty((steps + 1, *v0.shape), dtype=np.uint8)
    H = np.empty_like(V)
    V[0], H[0] = v0, h0
    for t in range(steps):
        V[t + 1], H[t + 1] = step(spec, V[t], H[t], t)
    return V, H


def random_state(rng: np.random.Generator, spec: WorldSpec, n: int, density: float = 0.5):
    """Random visible soup plus the initial hidden field the spec prescribes
    (zeros, or a hidden random draw for h0 == "random")."""
    v0 = (rng.random((n, n)) < density).astype(np.uint8)
    return v0, h0_field(spec, rng, v0.shape)
