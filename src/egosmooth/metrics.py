from __future__ import annotations
import numpy as np

DT = 0.5

def _finite(*arrays):
    if any(not np.isfinite(np.asarray(x)).all() for x in arrays):
        raise ValueError("metric input contains NaN or Inf")

def ade_fde(pred, gt):
    pred, gt = np.asarray(pred, np.float64), np.asarray(gt, np.float64)
    _finite(pred, gt)
    d = np.linalg.norm(pred - gt, axis=-1)
    return d.mean(axis=-1), d[..., -1]

def third_difference_vectors(points, dt=DT):
    p = np.asarray(points, np.float64)
    _finite(p)
    return (p[..., 3:, :] - 3*p[..., 2:-1, :] + 3*p[..., 1:-2, :] - p[..., :-3, :]) / dt**3

def jerk_decomposition(history_xy, future_xy, dt=DT):
    h, f = np.asarray(history_xy, np.float64), np.asarray(future_xy, np.float64)
    sequence = np.concatenate([h[..., -3:, :], f], axis=-2)
    vectors = third_difference_vectors(sequence, dt)
    terms = np.linalg.norm(vectors, axis=-1)
    return {
        "vectors": vectors,
        "terms": terms,
        "cross_boundary": terms[..., :3].mean(-1),
        "future_internal": terms[..., 3:].mean(-1),
        "history_aware_mean": terms.mean(-1),
        "history_aware_rms": np.sqrt(np.mean(terms**2, axis=-1)),
    }

def gt_third_difference_error(history_xy, pred, gt, dt=DT):
    pred_j = jerk_decomposition(history_xy, pred, dt)["vectors"]
    gt_j = jerk_decomposition(history_xy, gt, dt)["vectors"]
    terms = np.linalg.norm(pred_j - gt_j, axis=-1)
    return {"terms": terms, "six_term_mean": terms.mean(-1), "cross_boundary": terms[..., :3].mean(-1), "future_internal": terms[..., 3:].mean(-1)}

def boundary_errors(history_xy, pred, dt=DT):
    h, p = np.asarray(history_xy, np.float64), np.asarray(pred, np.float64)
    _finite(h, p)
    v_hist = (h[..., -1, :] - h[..., -2, :]) / dt
    v_pred = (p[..., 0, :] - h[..., -1, :]) / dt
    a_hist = (h[..., -1, :] - 2*h[..., -2, :] + h[..., -3, :]) / dt**2
    a_pred = (p[..., 1, :] - 2*p[..., 0, :] + h[..., -1, :]) / dt**2
    return {"velocity_boundary_error": np.linalg.norm(v_pred-v_hist, axis=-1), "acceleration_boundary_error": np.linalg.norm(a_pred-a_hist, axis=-1)}

def endpoint_shift(raw, smoothed):
    raw, smoothed = np.asarray(raw, np.float64), np.asarray(smoothed, np.float64)
    _finite(raw, smoothed)
    return np.linalg.norm(smoothed[..., -1, :] - raw[..., -1, :], axis=-1)

def summary(history_xy, pred, gt, raw=None):
    ade, fde = ade_fde(pred, gt)
    jerk = jerk_decomposition(history_xy, pred)
    boundary = boundary_errors(history_xy, pred)
    gt_error = gt_third_difference_error(history_xy, pred, gt)
    out = {
        "ade": ade,
        "fde": fde,
        "history_aware_mean_jerk": jerk["history_aware_mean"],
        "cross_boundary_jerk": jerk["cross_boundary"],
        "future_internal_jerk": jerk["future_internal"],
        "third_difference_error": gt_error["six_term_mean"],
        **boundary,
    }
    if raw is not None:
        out["endpoint_shift"] = endpoint_shift(raw, pred)
    return out
