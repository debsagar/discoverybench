"""The scripted theorist: induction by positing a latent.

Hypothesis = (driver, param, machine m: (H,2)->H, h0 mode). Given a
hypothesis, every cell's hidden trajectory follows from the visible frames
(exactly, when h0 == "zero"; by per-cell inference when h0 == "random"), so
the rule tables are fitted by COUNTING and the hypothesis is scored by its
training error. Class selection = MDL: train_err + class_bits / n_samples.

Never touches ground-truth h. Shares `signal` with the simulator so a
hypothesis means the same thing as the world it is about.
"""
import math

import numpy as np

from drivers import signal
from sim import neighbor_counts

EVAL_SKIP = 8          # held-out transitions scored for t >= EVAL_SKIP
SELECT_FRAMES = 128    # machine-selection cap (still budgeted data)
EM_ROUNDS = 3          # ponytail: fixed rounds; iterate-to-stable if a twist needs it
BEAM_FRAMES, BEAM_KEEP = 8, 128


def machines(H):
    for idx in range(H ** (2 * H)):
        m, x = np.empty((H, 2), np.uint8), idx
        for i in range(2 * H):
            m[i // 2, i % 2] = x % H
            x //= H
        yield m


_COUNTS = {}


def _counts(V):
    """Neighbor counts per frame, memoised per rollout array — the theorist
    revisits the same frames thousands of times (one pass per machine)."""
    key = id(V)          # safe only because the entry keeps V alive (address can't be reused)
    if key not in _COUNTS:
        if len(_COUNTS) > 256:
            _COUNTS.clear()
        _COUNTS[key] = (V, np.stack([neighbor_counts(V[t]) for t in range(V.shape[0])]))
    return _COUNTS[key][1]


def h_fields(machine, V, driver, param, h0=None):
    """h at each frame of V under the hypothesis (h0 zeros unless given)."""
    hs = np.empty_like(V)
    C = _counts(V)
    h = np.zeros(V.shape[1:], np.uint8) if h0 is None else h0
    for t in range(V.shape[0]):
        hs[t] = h
        h = machine[h, signal(driver, param, V[t], C[t], t)]
    return hs


def _idx(hs, V, t):
    return (hs[t].ravel(), V[t].ravel().astype(np.intp), _counts(V)[t].ravel())


def _count(counts, hs, V):
    for t in range(V.shape[0] - 1):
        np.add.at(counts, (*_idx(hs, V, t), V[t + 1].ravel().astype(np.intp)), 1)


def _cell_err(table, hs, V):
    """Per-cell number of mispredicted transitions along the whole of V."""
    e = np.zeros(V.shape[1:], np.int64)
    for t in range(V.shape[0] - 1):
        e += (table[_idx(hs, V, t)].reshape(V.shape[1:]) != V[t + 1])
    return e


def infer_h0(machine, table, V, driver, param):
    """Per-cell h0 in {0..H-1} minimising transition errors along V."""
    H = table.shape[0]
    errs = np.stack([_cell_err(table, h_fields(machine, V, driver, param,
                                                np.full(V.shape[1:], c, np.uint8)), V)
                     for c in range(H)])
    return errs.argmin(0).astype(np.uint8)


def fit_tables(machine, chunks, driver, param, H, infer=False):
    """(table (H,2,9), train_err). infer=True runs hard-EM over per-cell h0."""
    counts = np.zeros((H, 2, 9, 2), np.int64)
    fields = [h_fields(machine, V, driver, param) for V in chunks]
    for hs, V in zip(fields, chunks):
        _count(counts, hs, V)
    for _ in range(EM_ROUNDS if infer else 0):
        table = (counts[..., 1] > counts[..., 0]).astype(np.uint8)
        counts[:] = 0
        for V in chunks:
            h0 = infer_h0(machine, table, V, driver, param)
            _count(counts, h_fields(machine, V, driver, param, h0), V)
    table = (counts[..., 1] > counts[..., 0]).astype(np.uint8)
    return table, counts.min(axis=-1).sum() / max(counts.sum(), 1)


def held_err(machine, table, held, driver, param, infer=False):
    """Held-out error for t >= EVAL_SKIP; h0 inferred from the prefix only."""
    errs = tot = 0
    for V in held:
        h0 = infer_h0(machine, table, V[:EVAL_SKIP + 1], driver, param) if infer else None
        hs = h_fields(machine, V, driver, param, h0)
        for t in range(EVAL_SKIP, V.shape[0] - 1):
            p = table[_idx(hs, V, t)].reshape(V.shape[1:])
            errs += int((p != V[t + 1]).sum())
            tot += p.size
    return errs / tot


def _select_prefix(chunks, cap=SELECT_FRAMES):
    sel, used = [], 0
    for V in chunks:
        if used >= cap:
            break
        sel.append(V[: cap - used + 1])
        used += V.shape[0]
    return sel


def best_in_class(cands, sel, driver, param, H, infer=False):
    """Min-train-error machine among cands ("beam" = prune H=4 on a tiny prefix)."""
    if cands == "beam":
        tiny = [V[:BEAM_FRAMES + 1] for V in sel[:1]]
        cands = sorted(machines(H), key=lambda m: fit_tables(m, tiny, driver, param, H)[1])[:BEAM_KEEP]
    best_e, best_m = np.inf, None
    for m in cands:
        e = fit_tables(m, sel, driver, param, H, infer)[1]
        if e < best_e:
            best_e, best_m = e, m
    return best_e, best_m


def theorist_err(chunks, held, spec):
    """Class GIVEN by the spec (driver, param, H, h0 mode): the compressibility certificate."""
    infer = spec.h0 == "random"
    H, d, p = spec.n_hidden, spec.driver, spec.param
    _, m = best_in_class(list(machines(H)), _select_prefix(chunks), d, p, H, infer)
    table, _ = fit_tables(m, chunks, d, p, H, infer)
    return held_err(m, table, held, d, p, infer), m


# ---------- class union (for uncertain-class selection and the distinctness matrix) ----------

def classes():
    """(name, H, driver, param, machines|'beam'). h0 == 'zero' throughout;
    ponytail: add infer variants to the union once own_h0 worlds certify."""
    out = [("none", 1, "own", 0, [np.zeros((1, 2), np.uint8)])]
    for H in (2, 3):
        out.append((f"own(H={H})", H, "own", 0, list(machines(H))))
    out.append(("own(H=4)", 4, "own", 0, "beam"))
    for tau in range(1, 9):
        out.append((f"count(t{tau})", 2, "count", tau, list(machines(2))))
    for T in range(2, 9):
        out.append((f"clock(T{T})", 2, "clock", T, list(machines(2))))
    return out


def class_bits(H, cands):
    return 18 * H + (math.log2(len(cands)) if cands != "beam" else 16)


def select(chunks):
    """MDL pick over the union. Returns (name, H, driver, param, machine)."""
    sel = _select_prefix(chunks)
    n = sum((V.shape[0] - 1) * V[0].size for V in sel)
    best = None
    for name, H, d, p, cands in classes():
        e, m = best_in_class(cands, sel, d, p, H)
        score = e + class_bits(H, cands) / max(n, 1)
        if best is None or score < best[0]:
            best = (score, name, H, d, p, m)
    return best[1:]
