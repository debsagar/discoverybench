"""The null family (enumeration) and the budgeted data pools.

Enumerator k: majority-vote table over (3x3 pattern, own v at t-1..t-k),
fitted only on contexts that actually occurred; unseen context -> persistence.
Enumerator "t": table over (3x3 pattern, t mod T), best T in 1..32 by TRAIN
error — the strongest cheap null against clock worlds. Neither posits a latent.
"""
import numpy as np

from sim import rollout, random_state
from floor import patterns, N_PATTERNS
from theorist import EVAL_SKIP

ROLL_LEN = 32          # frames per training rollout chunk
KS = (0, 1, 2, 8, "t")
T_MAX = 32          # ponytail: = ROLL_LEN; a global cycle H·T can reach 24 at H=3, T=8


def train_pool(spec, seed, n_frames):
    rng = np.random.default_rng(seed)
    chunks, got = [], 0
    while got < n_frames:
        f = min(ROLL_LEN, n_frames - got)
        chunks.append(rollout(spec, *random_state(rng, spec, 32), f)[0])
        got += f
    return chunks


def held_out(spec, seed, n=4, steps=64):
    rng = np.random.default_rng(seed + 777_000)
    return [rollout(spec, *random_state(rng, spec, 32), steps)[0] for _ in range(n)]


def feats(V, k, t0, T=1):
    """(features, targets) for transitions t in [max(t0,k), len(V)-1)."""
    depth = 0 if k == "t" else k
    fs, ys = [], []
    for t in range(max(t0, depth), V.shape[0] - 1):
        f = patterns(V[t])
        if k == "t":
            f |= (t % T) << 9
        for j in range(1, depth + 1):
            f |= V[t - j].astype(np.int64) << (9 + j - 1)
        fs.append(f.ravel())
        ys.append(V[t + 1].ravel())
    if not fs:
        return np.empty(0, np.int64), np.empty(0, np.uint8)
    return np.concatenate(fs), np.concatenate(ys)


def _table(chunks, k, T):
    n_feat = N_PATTERNS * T if k == "t" else N_PATTERNS << k
    parts = [feats(V, k, 0, T) for V in chunks]
    f = np.concatenate([p[0] for p in parts])
    y = np.concatenate([p[1] for p in parts])
    if f.size == 0:
        return None, None, 1.0             # budget below context depth: no table
    counts = np.bincount(f * 2 + y, minlength=n_feat * 2).reshape(n_feat, 2)
    pred = (counts[:, 1] > counts[:, 0]).astype(np.uint8)
    return pred, counts.sum(1) > 0, counts.min(1).sum() / counts.sum()


def enumerator_err(chunks, held, k):
    Ts = range(1, T_MAX + 1) if k == "t" else (1,)
    _, T = min((_table(chunks, k, T)[2], T) for T in Ts)
    pred, seen, _ = _table(chunks, k, T)
    errs = tot = 0
    for V in held:
        f_te, y_te = feats(V, k, EVAL_SKIP, T)
        v_now = ((f_te >> 4) & 1).astype(np.uint8)       # persistence fallback
        p = v_now if pred is None else np.where(seen[f_te], pred[f_te], v_now)
        errs += int((p != y_te).sum())
        tot += y_te.size
    return errs / tot


def persistence_err(held):
    errs = tot = 0
    for V in held:
        for t in range(EVAL_SKIP, V.shape[0] - 1):
            errs += int((V[t] != V[t + 1]).sum())
            tot += V[t].size
    return errs / tot
