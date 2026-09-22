"""Module 3: the memory-depth floor.

Since h0 = 0 and h' = h_next[h][own v], each cell's hidden state is a
deterministic function of that cell's own visible history. So the hidden
variable is discoverable (a learnability guarantee, per the Tenenbaum
desiderata), and the honest claim is: a visible-only predictor must USE
HISTORY (or posit a latent) to predict well. What we measure is how much
history — the memory depth of each world.

Predictors, all majority-vote over discrete features, held-out evaluation:

  err(k), k=0,1,2,4,8 : feature = 3x3 visible pattern at t (order-1, 512
        values) plus the cell's OWN visible state at t-1..t-k. err(0) is the
        best order-1 3x3 visible predictor — note "order-1 3x3", not "best
        visible-only": a wider window or deeper history recovers more of h.
  err_h : feature = (pattern, true h). Deterministic => must be ~0. Control
        proving the k=0 residual is attributable to hiddenness.

The err(k) curve is the difficulty axis: worlds where the gap dies at k=1
are just two-state cells; worlds where it survives to k=8 are the hard ones.

Degeneracy diagnostics (reviewer point 3): a world can nominally have H=3
while its effective H is 1 (unreachable states, near-identical tables).
  h_occupancy      : empirical distribution of h on held-out rollouts
  rule_disagreement: max over occupied h-pairs of P_pattern~test[outcome
                     under h1 != outcome under h2] — do the tables that are
                     actually in play differ on patterns that actually occur?

All ks share identical train/test transitions (t >= max k), so the curve is
comparable across k.
"""

import numpy as np

from spec import WorldSpec
from sim import rollout, random_state

N_PATTERNS = 512          # 2^9 possible 3x3 binary patterns
KS = (0, 1, 2, 4, 8)      # own-cell history depths
MAX_K = max(KS)
OCCUPIED = 0.05           # h state counts as "in play" above this occupancy


def patterns(v: np.ndarray) -> np.ndarray:
    """Encode each cell's 3x3 visible neighborhood as an int in [0, 512)."""
    p = np.zeros(v.shape, dtype=np.int64)
    bit = 0
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            p |= np.roll(np.roll(v, dy, axis=0), dx, axis=1).astype(np.int64) << bit
            bit += 1
    return p


def _fit(feat, target, n_feat):
    counts = np.bincount(feat * 2 + target, minlength=n_feat * 2).reshape(n_feat, 2)
    return (counts[:, 1] > counts[:, 0]).astype(np.uint8)


def _collect(spec, rng, n_rollouts, steps, grid):
    """Per-rollout stacked arrays: 3x3 pattern ids P, hidden H, visible V."""
    out = []
    for _ in range(n_rollouts):
        V, H = rollout(spec, *random_state(rng, spec, grid), steps)
        P = np.stack([patterns(V[t]) for t in range(steps)])
        out.append((P, H, V))
    return out


def _features(rollouts, k, steps):
    """Transitions t -> t+1 for t in [MAX_K, steps): feature = pattern at t
    | own v at t-1..t-k shifted above the 9 pattern bits. Same t-range for
    every k, so all depths score on identical transitions."""
    feats, ys, hs = [], [], []
    for P, H, V in rollouts:
        for t in range(MAX_K, steps):
            f = P[t].copy()
            for j in range(1, k + 1):
                f |= V[t - j].astype(np.int64) << (9 + j - 1)
            feats.append(f.ravel())
            ys.append(V[t + 1].ravel())
            hs.append(H[t].ravel())
    return np.concatenate(feats), np.concatenate(ys), np.concatenate(hs)


def _outcome_table(spec):
    """O[h, p]: the deterministic next center state for each 3x3 pattern and
    hidden state (center = bit 4, neighbor count = popcount minus center)."""
    p = np.arange(N_PATTERNS)
    center = (p >> 4) & 1
    count = np.bitwise_count(p) - center
    return np.where(center == 1, spec.survive[:, count], spec.birth[:, count])


def markov_floor(spec: WorldSpec, seed: int = 0, n_train: int = 8, n_test: int = 4,
                 steps: int = 64, grid: int = 32) -> dict:
    rng = np.random.default_rng(seed)
    H = spec.n_hidden
    train = _collect(spec, rng, n_train, steps, grid)
    test = _collect(spec, rng, n_test, steps, grid)

    errs = {}
    for k in KS:
        n_feat = N_PATTERNS << k
        f_tr, y_tr, _ = _features(train, k, steps)
        f_te, y_te, h_te = _features(test, k, steps)
        pred = _fit(f_tr, y_tr, n_feat)
        errs[k] = float(np.mean(pred[f_te] != y_te))

    # Control: with true h in the feature the process is deterministic.
    f_tr, y_tr, h_tr = _features(train, 0, steps)
    f_te, y_te, h_te = _features(test, 0, steps)
    pred_h = _fit(f_tr * H + h_tr, y_tr, N_PATTERNS * H)
    err_h = float(np.mean(pred_h[f_te * H + h_te] != y_te))

    # Degeneracy diagnostics on held-out transitions.
    occ = np.bincount(h_te, minlength=H) / h_te.size
    freq = np.bincount(f_te, minlength=N_PATTERNS) / f_te.size
    O = _outcome_table(spec)
    live = [i for i in range(H) if occ[i] >= OCCUPIED]
    disagreement = max((float(freq @ (O[a] != O[b]))
                        for i, a in enumerate(live) for b in live[i + 1:]), default=0.0)

    v_te = (f_te >> 4) & 1
    return {
        "err": errs,                                    # err[k] for k in KS
        "err_h": err_h,                                 # control, ~0
        "persistence_err": float(np.mean(v_te != y_te)),
        "activity": float(np.mean(y_te)),
        "h_occupancy": occ.round(3).tolist(),
        "effective_H": len(live),
        "rule_disagreement": disagreement,
    }
