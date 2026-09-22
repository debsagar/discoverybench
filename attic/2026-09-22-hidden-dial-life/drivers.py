"""The twist axis: what drives the hidden state.

Every world updates its hidden state as  h' = m[h, d]  with a BINARY driver
signal d. The twist is which signal:

  own        d = v                    cell remembers its own past
  count(tau) d = 1{count >= tau}      cell remembers its crowd
  clock(T)   d = 1{(t+1) mod T == 0}  a global tick; h is the same everywhere

plus, orthogonally, how h starts: h0 == "zero" (h reconstructible from
history) or "random" (per-cell hidden h0 that must be INFERRED).

Shared by the simulator (ground truth) and the theorist (hypothesis), so the
two can never disagree about what a driver means.
"""
import numpy as np

DRIVERS = ("own", "count", "clock")


def signal(driver: str, param: int, v: np.ndarray, count: np.ndarray, t: int) -> np.ndarray:
    if driver == "own":
        return v
    if driver == "count":
        return (count >= param).astype(np.uint8)
    if driver == "clock":
        return np.full(v.shape, (t + 1) % param == 0, np.uint8)
    raise ValueError(f"unknown driver {driver!r}")


def h0_field(spec, rng: np.random.Generator, shape) -> np.ndarray:
    if spec.h0 == "random":
        return rng.integers(0, spec.n_hidden, size=shape, dtype=np.uint8)
    return np.zeros(shape, np.uint8)
