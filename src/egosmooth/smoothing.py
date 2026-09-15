from __future__ import annotations
import numpy as np

def raw(p, **_):
    return np.asarray(p, np.float64).copy()

def moving_average(p, window):
    p = np.asarray(p, np.float64)
    radius = window // 2
    return np.stack([p[max(0, i-radius):min(len(p), i+radius+1)].mean(0) for i in range(len(p))])

def exponential_blend(p, alpha):
    p = np.asarray(p, np.float64)
    q = p.copy()
    for i in range(1, len(q)):
        q[i] = alpha * p[i] + (1.0 - alpha) * q[i-1]
    return q

def laplacian(p, lam):
    p = np.asarray(p, np.float64)
    q = p.copy()
    q[1:-1] = p[1:-1] + lam * (p[:-2] - 2.0 * p[1:-1] + p[2:])
    return q

def savitzky_golay(p, window, polyorder):
    p = np.asarray(p, np.float64)
    if window % 2 != 1 or window <= polyorder or window > len(p):
        raise ValueError("invalid SG window/polyorder")
    half = window // 2
    out = np.empty_like(p)
    for coordinate in range(2):
        for i in range(len(p)):
            if i < half:
                idx = np.arange(window)
            elif i >= len(p) - half:
                idx = np.arange(len(p) - window, len(p))
            else:
                idx = np.arange(i-half, i+half+1)
            coef = np.polyfit(idx - i, p[idx, coordinate], polyorder)
            out[i, coordinate] = np.polyval(coef, 0.0)
    return out

def quadratic_regularization(p, lam):
    """Minimise ||q-p||² + lam||D2 q||² while fixing both endpoints."""
    p = np.asarray(p, np.float64)
    n = len(p)
    d2 = np.zeros((n-2, n), np.float64)
    for i in range(n-2):
        d2[i, i:i+3] = (1.0, -2.0, 1.0)
    a = np.eye(n) + lam * (d2.T @ d2)
    interior = np.arange(1, n-1)
    boundary = np.asarray([0, n-1])
    q = p.copy()
    rhs = p[interior] - a[np.ix_(interior, boundary)] @ p[boundary]
    q[interior] = np.linalg.solve(a[np.ix_(interior, interior)], rhs)
    return q

def apply_candidate(p, candidate):
    family = candidate["family"]
    params = candidate.get("params", {})
    return {
        "Raw": raw,
        "MovingAverage": moving_average,
        "ExponentialBlend": exponential_blend,
        "Laplacian": laplacian,
        "SavitzkyGolay": savitzky_golay,
        "QuadraticRegularization": quadratic_regularization,
    }[family](p, **params)
