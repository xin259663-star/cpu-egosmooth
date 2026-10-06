"""Build an auditable real-BEV qualitative Fig. 3 from frozen held-out assets.

This script performs deterministic posthoc selection only. It never trains a model,
changes trajectories, smooths GT/Raw predictions, or invents map geometry/metrics.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
import tarfile
from pathlib import Path


def _bootstrap_recovered_dependencies(root: Path) -> None:
    deps = root / "work/p1_evidence_revision/recovery_search/python_deps"
    if deps.exists():
        dll_dir = deps / "pyarrow"
        if os.name == "nt" and dll_dir.exists():
            os.add_dll_directory(str(dll_dir))
        sys.path.insert(0, str(deps))


DEFAULT_ROOT = Path(".")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Default: ROOT/work/posthoc_submission_review/fig3_real_bev_redraw",
    )
    parser.add_argument(
        "--map-archive",
        type=Path,
        default=Path("data/v1.0-trainval_meta.tgz"),
    )
    return parser.parse_args()


ARGS = parse_args()
ROOT = ARGS.root
_bootstrap_recovered_dependencies(ROOT)

import ijson  # noqa: E402
import matplotlib  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from PIL import Image  # noqa: E402


matplotlib.use("Agg")
Image.MAX_IMAGE_PIXELS = None

OUTPUT = (
    ARGS.output_dir
    if ARGS.output_dir
    else ROOT / "work/posthoc_submission_review/fig3_real_bev_redraw"
)
PAYLOAD_PATH = (
    ROOT
    / "work/p2_log_grouped_replication/13_heldout_evaluation/preflight/heldout_payloads"
    / "log_primary/heldout.npz"
)
PROVENANCE_PATH = PAYLOAD_PATH.with_name("heldout_provenance.parquet")
METRICS_PATH = (
    ROOT
    / "work/p2_log_grouped_replication/13_heldout_evaluation/sample_metrics"
    / "log_primary/heldout_sample_metrics.parquet"
)
PREDICTIONS_ROOT = (
    ROOT
    / "work/p2_log_grouped_replication/13_heldout_evaluation/predictions/log_primary"
)
SELECTION_ROOT = ROOT / "work/p2_log_grouped_replication/metrics/validation_b"
META_ROOT = (
    ROOT
    / "work/p1_evidence_revision/reconstructed_metadata/official_meta_extract/v1.0-trainval"
)

STRATEGY_RAW = "Raw"
STRATEGY_FIXED = "Fixed SG(5,2)"
STRATEGY_SELECTED = "Validation-B-selected"
KEY = ["run_id", "scene_token", "sample_token"]
METRICS = ["ade", "fde", "history_aware_mean_jerk"]


def require_paths() -> None:
    required = [
        PAYLOAD_PATH,
        PROVENANCE_PATH,
        METRICS_PATH,
        PREDICTIONS_ROOT,
        SELECTION_ROOT,
        META_ROOT / "sample.json",
        META_ROOT / "sample_data.json",
        META_ROOT / "ego_pose.json",
        META_ROOT / "scene.json",
        META_ROOT / "log.json",
        META_ROOT / "map.json",
        META_ROOT / "sensor.json",
        META_ROOT / "calibrated_sensor.json",
        ARGS.map_archive,
    ]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError("Required assets missing:\n" + "\n".join(missing))


def load_selected_smoothers(run_ids: list[str]) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for run_id in run_ids:
        path = SELECTION_ROOT / run_id / "selected_smoother.json"
        if not path.exists():
            raise FileNotFoundError(path)
        obj = json.loads(path.read_text(encoding="utf-8"))
        candidate = obj.get("selected_candidate")
        if not isinstance(candidate, dict) or "id" not in candidate:
            raise KeyError(f"Unexpected selected_smoother schema: {path}")
        rows.append(
            {
                "run_id": run_id,
                "selected_smoother": str(candidate["id"]),
                "selected_family": str(candidate.get("family", "")),
                "selected_params": json.dumps(candidate.get("params", {}), sort_keys=True),
                "endpoints_fixed": bool(candidate.get("endpoints_fixed", False)),
            }
        )
    return pd.DataFrame(rows)


def robust_scale(frame: pd.DataFrame, columns: list[str]) -> tuple[pd.DataFrame, dict]:
    scaled = pd.DataFrame(index=frame.index)
    audit: dict[str, dict[str, float | bool]] = {}
    for column in columns:
        values = frame[column].astype(float)
        median = float(values.median())
        q1 = float(values.quantile(0.25))
        q3 = float(values.quantile(0.75))
        iqr = q3 - q1
        used = iqr if iqr > 1e-15 else 1.0
        scaled[column] = (values - median) / used
        audit[column] = {
            "median": median,
            "q1": q1,
            "q3": q3,
            "iqr": iqr,
            "zero_iqr_fallback_to_one": bool(iqr <= 1e-15),
        }
    return scaled, audit


def validate_and_pivot_metrics(metrics: pd.DataFrame) -> pd.DataFrame:
    required = set(KEY + ["window_index", "log_token", "model", "seed", "strategy"] + METRICS)
    missing = sorted(required - set(metrics.columns))
    if missing:
        raise KeyError(f"Metric fields missing: {missing}; actual={metrics.columns.tolist()}")
    if len(metrics) != 435150:
        raise AssertionError(f"Expected 435150 metric rows, found {len(metrics)}")
    run_ids = sorted(metrics["run_id"].unique().tolist())
    if len(run_ids) != 50:
        raise AssertionError(f"Expected 50 formal runs, found {len(run_ids)}")
    counts = metrics.groupby(["run_id", "strategy"], observed=True).size()
    if not (counts == 2901).all():
        raise AssertionError(f"Expected 2901 rows per run-strategy; violations:\n{counts[counts != 2901]}")
    if metrics.duplicated(KEY + ["strategy"]).any():
        raise AssertionError("Duplicate run_id + scene_token + sample_token + strategy key")
    wide = metrics.pivot(index=KEY, columns="strategy", values=METRICS)
    expected = {(m, s) for m in METRICS for s in [STRATEGY_RAW, STRATEGY_FIXED, STRATEGY_SELECTED]}
    if set(wide.columns) != expected:
        raise AssertionError(f"Unexpected strategy/metric columns: {wide.columns.tolist()}")
    wide.columns = [f"{metric}__{strategy}" for metric, strategy in wide.columns]
    wide = wide.reset_index()
    metadata = metrics.loc[
        metrics.strategy == STRATEGY_RAW,
        KEY + ["window_index", "log_token", "model", "seed"],
    ]
    wide = wide.merge(metadata, on=KEY, validate="one_to_one", how="left")
    if wide[["window_index", "log_token", "model", "seed"]].isna().any().any():
        raise AssertionError("Missing metric metadata after pivot")
    return wide


def add_effect_columns(wide: pd.DataFrame) -> pd.DataFrame:
    out = wide.copy()
    for metric in METRICS:
        short = {"ade": "ade", "fde": "fde", "history_aware_mean_jerk": "shape"}[metric]
        out[f"delta_{short}_FR"] = out[f"{metric}__{STRATEGY_FIXED}"] - out[f"{metric}__{STRATEGY_RAW}"]
        out[f"delta_{short}_SF"] = out[f"{metric}__{STRATEGY_SELECTED}"] - out[f"{metric}__{STRATEGY_FIXED}"]
    return out


def rank_reference_runs(wide: pd.DataFrame, smoother_df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    effect_cols = [
        "delta_ade_FR",
        "delta_fde_FR",
        "delta_shape_FR",
        "delta_ade_SF",
        "delta_fde_SF",
        "delta_shape_SF",
    ]
    grouped = wide.groupby(["run_id", "model", "seed"], as_index=False)[effect_cols].mean()
    grouped = grouped.merge(smoother_df, on="run_id", validate="one_to_one")
    scaled, scale_audit = robust_scale(grouped, effect_cols)
    grouped["distance_to_median"] = np.sqrt(np.square(scaled[effect_cols]).sum(axis=1))
    grouped["eligible_reference"] = grouped.selected_smoother.isin(["qreg_l1", "qreg_l01"])
    grouped = grouped.sort_values(
        ["eligible_reference", "distance_to_median", "run_id"],
        ascending=[False, True, True],
        kind="mergesort",
    ).reset_index(drop=True)
    grouped["rank"] = np.arange(1, len(grouped) + 1)
    eligible = grouped[grouped.eligible_reference]
    if eligible.empty:
        raise AssertionError("No qreg_l1/qreg_l01 reference-run candidate")
    chosen = eligible.iloc[0].to_dict()
    grouped.to_csv(OUTPUT / "fig3_reference_run_ranking.csv", index=False)
    return grouped, {"robust_scale": scale_audit, "selected": chosen}


def _choose_unique(candidates: pd.DataFrame, used: set[tuple[str, str]], sort_cols, ascending) -> pd.Series:
    candidates = candidates.copy()
    candidates["_used"] = [
        (str(s), str(t)) in used for s, t in zip(candidates.scene_token, candidates.sample_token)
    ]
    available = candidates[~candidates._used]
    if available.empty:
        raise AssertionError("No unique case remains for deterministic panel selection")
    return available.sort_values(sort_cols, ascending=ascending, kind="mergesort").iloc[0]


def select_cases(run_wide: pd.DataFrame, selected_smoother: str) -> tuple[pd.DataFrame, dict]:
    run_wide = run_wide.replace([np.inf, -np.inf], np.nan).dropna(
        subset=["delta_ade_FR", "delta_fde_FR", "delta_shape_FR", "delta_ade_SF", "delta_fde_SF", "delta_shape_SF"]
    )
    if len(run_wide) != 2901:
        raise AssertionError(f"Non-finite per-window effects: kept {len(run_wide)} of 2901")
    used: set[tuple[str, str]] = set()
    picked: list[pd.Series] = []
    audit: dict[str, object] = {"manual_override": False}

    # Frozen-trajectory display score used only to break panel-(b) candidates
    # toward a case whose Raw-vs-Fixed geometry is visibly separable. This is
    # deterministic posthoc selection; no trajectory or metric is altered.
    run_id = str(run_wide.run_id.iloc[0])
    run_dir = PREDICTIONS_ROOT / run_id
    raw_display = load_prediction_file(run_dir / "raw_predictions.npz")
    fixed_display = load_prediction_file(run_dir / "fixed_sg_predictions.npz")
    key_to_prediction_index = {
        (str(scene), str(sample)): i
        for i, (scene, sample) in enumerate(zip(raw_display["scene_token"], raw_display["sample_token"]))
    }
    display_scores = []
    for scene, sample in zip(run_wide.scene_token, run_wide.sample_token):
        idx = key_to_prediction_index[(str(scene), str(sample))]
        pointwise = np.linalg.norm(
            fixed_display["prediction"][idx] - raw_display["prediction"][idx], axis=1
        )
        display_scores.append(float(pointwise.max() + 0.5 * pointwise.mean()))
    run_wide = run_wide.copy()
    run_wide["raw_fixed_display_separation"] = display_scores

    neg = run_wide[run_wide.delta_shape_FR < 0].copy()
    med_neg = float(neg.delta_shape_FR.median())
    neg["shape_median_distance"] = (neg.delta_shape_FR - med_neg).abs()
    neg["accuracy_tie"] = neg.delta_ade_FR.abs() + neg.delta_fde_FR.abs()
    a = _choose_unique(neg, used, ["shape_median_distance", "accuracy_tie", "scene_token", "sample_token"], [True] * 4)
    used.add((str(a.scene_token), str(a.sample_token)))
    picked.append(a)
    audit["panel_a"] = {
        "criterion": "Closest negative Fixed-minus-Raw Shape change to the negative-change median; accuracy-change tie-break.",
        "median_negative_delta_shape_FR": med_neg,
        "negative_candidate_count": int(len(neg)),
    }

    q1, q3 = run_wide.delta_shape_FR.quantile([0.25, 0.75]).astype(float)
    outer_fence = float(q1 - 3.0 * (q3 - q1))
    b = None
    b_threshold: dict[str, object] = {}
    for quantile in [0.10, 0.15, 0.20]:
        ade_thr = float(run_wide.delta_ade_FR.abs().quantile(quantile))
        fde_thr = float(run_wide.delta_fde_FR.abs().quantile(quantile))
        cand = run_wide[
            (run_wide.delta_ade_FR.abs() <= ade_thr)
            & (run_wide.delta_fde_FR.abs() <= fde_thr)
            & (run_wide.delta_shape_FR < 0)
            & (run_wide.delta_shape_FR >= outer_fence)
        ].copy()
        cand = cand[
            ~pd.MultiIndex.from_frame(cand[["scene_token", "sample_token"]]).isin(
                pd.MultiIndex.from_tuples(list(used), names=["scene_token", "sample_token"])
            )
        ]
        if not cand.empty:
            b = cand.sort_values(
                ["raw_fixed_display_separation", "delta_shape_FR", "scene_token", "sample_token"],
                ascending=[False, True, True, True],
                kind="mergesort",
            ).iloc[0]
            b_threshold = {
                "quantile_used": quantile,
                "abs_delta_ADE_threshold": ade_thr,
                "abs_delta_FDE_threshold": fde_thr,
                "Tukey_outer_fence_delta_shape_FR": outer_fence,
                "candidate_count": int(len(cand)),
            }
            break
    if b is None:
        raise AssertionError("Panel (b) candidate set empty after specified 10/15/20% fallbacks")
    used.add((str(b.scene_token), str(b.sample_token)))
    picked.append(b)
    audit["panel_b"] = {
        "criterion": "Small Fixed-minus-Raw ADE/FDE change with maximum visible Raw-vs-Fixed trajectory separation; negative non-outer-fence Shape change required.",
        **b_threshold,
    }

    pos_ade = run_wide.loc[run_wide.delta_ade_FR > 0, "delta_ade_FR"]
    pos_fde = run_wide.loc[run_wide.delta_fde_FR > 0, "delta_fde_FR"]
    if pos_ade.empty or pos_fde.empty:
        raise AssertionError("Panel (c) needs positive ADE and FDE tails")
    p95_ade = float(pos_ade.quantile(0.95))
    p95_fde = float(pos_fde.quantile(0.95))
    cbase = run_wide.copy()
    cbase["r_ADE"] = np.where(cbase.delta_ade_FR > 0, cbase.delta_ade_FR / p95_ade, 0.0)
    cbase["r_FDE"] = np.where(cbase.delta_fde_FR > 0, cbase.delta_fde_FR / p95_fde, 0.0)
    cbase["severity"] = cbase[["r_ADE", "r_FDE"]].max(axis=1)
    c = None
    severity_band = None
    for lo, hi in [(0.90, 1.10), (0.80, 1.20)]:
        cand = cbase[(cbase.severity >= lo) & (cbase.severity <= hi)].copy()
        cand = cand[
            ~pd.MultiIndex.from_frame(cand[["scene_token", "sample_token"]]).isin(
                pd.MultiIndex.from_tuples(list(used), names=["scene_token", "sample_token"])
            )
        ]
        if not cand.empty:
            cand["shape_preference"] = (cand.delta_shape_FR >= 0).astype(int)
            cand["severity_distance"] = (cand.severity - 1.0).abs()
            c = cand.sort_values(
                ["shape_preference", "severity_distance", "scene_token", "sample_token"],
                kind="mergesort",
            ).iloc[0]
            severity_band = [lo, hi]
            break
    if c is None:
        raise AssertionError("Panel (c) has no candidate in specified severity bands")
    used.add((str(c.scene_token), str(c.sample_token)))
    picked.append(c)
    audit["panel_c"] = {
        "criterion": "Fixed-minus-Raw positive-tail severity nearest one, preferring negative Shape change.",
        "P95_positive_delta_ADE": p95_ade,
        "P95_positive_delta_FDE": p95_fde,
        "severity_band_used": severity_band,
    }

    dbase = run_wide.copy()
    sf_cols = ["delta_ade_SF", "delta_fde_SF", "delta_shape_SF"]
    medians = dbase[sf_cols].median()
    iqr = dbase[sf_cols].quantile(0.75) - dbase[sf_cols].quantile(0.25)
    scale = iqr.mask(iqr <= 1e-15, 1.0)
    dbase["sf_median_distance"] = np.sqrt(
        np.square((dbase[sf_cols] - medians) / scale).sum(axis=1)
    )
    preferred = dbase[
        (dbase.delta_ade_SF < 0) & (dbase.delta_fde_SF > 0) & (dbase.delta_shape_SF < 0)
    ].copy()
    fallback = None
    sign_counts = None
    if preferred.empty:
        signs = pd.DataFrame(
            {
                "ade_sign": np.sign(dbase.delta_ade_SF).astype(int),
                "fde_sign": np.sign(dbase.delta_fde_SF).astype(int),
                "shape_sign": np.sign(dbase.delta_shape_SF).astype(int),
            }
        )
        sign_counts = signs.value_counts().reset_index(name="count").to_dict(orient="records")
        top = sign_counts[0]
        preferred = dbase[
            (np.sign(dbase.delta_ade_SF) == top["ade_sign"])
            & (np.sign(dbase.delta_fde_SF) == top["fde_sign"])
            & (np.sign(dbase.delta_shape_SF) == top["shape_sign"])
        ].copy()
        fallback = "Most frequent observed sign pattern"
    d = _choose_unique(preferred, used, ["sf_median_distance", "scene_token", "sample_token"], [True] * 3)
    picked.append(d)
    audit["panel_d"] = {
        "criterion": "Selected-minus-Fixed sign pattern (-,+,-), then robust distance to the all-window median effect vector.",
        "selected_smoother": selected_smoother,
        "median_vector": {k: float(v) for k, v in medians.items()},
        "iqr_vector": {k: float(v) for k, v in iqr.items()},
        "preferred_candidate_count": int(len(preferred)),
        "fallback": fallback,
        "sign_combinations_if_fallback": sign_counts,
    }

    cases = pd.DataFrame(picked).reset_index(drop=True)
    cases.insert(0, "panel", ["a", "b", "c", "d"])
    cases.insert(
        1,
        "panel_title",
        [
            "Typical geometry reduction",
            "Accuracy preserved, geometry altered",
            "Local error increase",
            "Selected differs from Fixed SG",
        ],
    )
    cases.insert(2, "panel_note", ["median ΔShape case", "small ΔADE/FDE", "positive-tail case", f"{selected_smoother} vs SG(5,2)"])
    return cases, audit


def load_prediction_file(path: Path) -> dict[str, np.ndarray]:
    if not path.exists():
        raise FileNotFoundError(path)
    with np.load(path, allow_pickle=False) as data:
        required = {"prediction", "scene_token", "sample_token", "window_index", "run_id"}
        missing = required - set(data.files)
        if missing:
            raise KeyError(f"Missing prediction keys {sorted(missing)} in {path}; actual={data.files}")
        return {key: data[key] for key in data.files}


def validate_prediction_alignment(pred: dict[str, np.ndarray], payload: dict[str, np.ndarray], run_id: str) -> None:
    if pred["prediction"].shape != (2901, 6, 2):
        raise AssertionError(f"Prediction shape mismatch: {pred['prediction'].shape}")
    if str(np.asarray(pred["run_id"]).reshape(-1)[0]) != run_id:
        raise AssertionError("Prediction run_id mismatch")
    checks = {
        "scene_token": payload["scene_token"],
        "sample_token": payload["anchor_sample_token"],
        "window_index": payload["window_index"],
    }
    for key, expected in checks.items():
        if not np.array_equal(pred[key], expected):
            mismatch = np.flatnonzero(pred[key] != expected)[:10].tolist()
            raise AssertionError(f"Prediction alignment mismatch for {key}: {mismatch}")


def attach_trajectories_and_recompute(cases: pd.DataFrame, run_id: str) -> tuple[pd.DataFrame, dict[str, np.ndarray]]:
    with np.load(PAYLOAD_PATH, allow_pickle=False) as loaded:
        payload = {key: loaded[key] for key in loaded.files}
    if payload["history_xy"].shape != (2901, 4, 2) or payload["future_xy"].shape != (2901, 6, 2):
        raise AssertionError("Held-out trajectory shapes do not match the frozen schema")
    if len(np.unique(payload["scene_token"])) != 93 or len(np.unique(payload["log_token"])) != 7:
        raise AssertionError("Expected 93 held-out scenes and 7 held-out logs")
    run_dir = PREDICTIONS_ROOT / run_id
    preds = {
        "raw": load_prediction_file(run_dir / "raw_predictions.npz"),
        "fixed": load_prediction_file(run_dir / "fixed_sg_predictions.npz"),
        "selected": load_prediction_file(run_dir / "selected_predictions.npz"),
    }
    for pred in preds.values():
        validate_prediction_alignment(pred, payload, run_id)
    index_by_key = {
        (str(scene), str(sample)): i
        for i, (scene, sample) in enumerate(zip(payload["scene_token"], payload["anchor_sample_token"]))
    }
    if len(index_by_key) != 2901:
        raise AssertionError("Held-out scene_token + anchor_sample_token is not unique")
    arrays: dict[str, list[np.ndarray]] = {k: [] for k in ["history", "gt", "raw", "fixed", "selected"]}
    recomputed_rows: list[dict[str, float]] = []
    for _, row in cases.iterrows():
        key = (str(row.scene_token), str(row.sample_token))
        if key not in index_by_key:
            raise AssertionError(f"Selected case missing from held-out payload: {key}")
        idx = index_by_key[key]
        arrays["history"].append(payload["history_xy"][idx].astype(float))
        arrays["gt"].append(payload["future_xy"][idx].astype(float))
        for name in ["raw", "fixed", "selected"]:
            arrays[name].append(preds[name]["prediction"][idx].astype(float))
        recomputed: dict[str, float] = {}
        for name in ["raw", "fixed", "selected"]:
            distances = np.linalg.norm(arrays[name][-1] - arrays["gt"][-1], axis=1)
            recomputed[f"ADE_{name}_recomputed"] = float(distances.mean())
            recomputed[f"FDE_{name}_recomputed"] = float(distances[-1])
            metric_suffix = {"raw": STRATEGY_RAW, "fixed": STRATEGY_FIXED, "selected": STRATEGY_SELECTED}[name]
            for metric_name, computed_name in [("ade", "ADE"), ("fde", "FDE")]:
                official = float(row[f"{metric_name}__{metric_suffix}"])
                computed = recomputed[f"{computed_name}_{name}_recomputed"]
                if abs(official - computed) > 1e-5:
                    raise RuntimeError(
                        f"METRIC_RECOMPUTE_MISMATCH panel={row.panel} strategy={name} "
                        f"metric={metric_name} official={official:.12g} computed={computed:.12g}"
                    )
        recomputed_rows.append(recomputed)
    stacked = {name: np.stack(values) for name, values in arrays.items()}
    for name, array in stacked.items():
        expected = (4, 4, 2) if name == "history" else (4, 6, 2)
        if array.shape != expected or not np.isfinite(array).all():
            raise AssertionError(f"Invalid selected trajectory array {name}: {array.shape}")
    cases = pd.concat([cases.reset_index(drop=True), pd.DataFrame(recomputed_rows)], axis=1)
    return cases, stacked


def load_small_json(name: str) -> list[dict]:
    return json.loads((META_ROOT / name).read_text(encoding="utf-8"))


def stream_json_records(path: Path, predicate, wanted_count: int) -> list[dict]:
    found: list[dict] = []
    with path.open("rb") as stream:
        for record in ijson.items(stream, "item"):
            if predicate(record):
                found.append(record)
                if len(found) == wanted_count:
                    break
    if len(found) != wanted_count:
        raise AssertionError(f"Found {len(found)} of {wanted_count} required records in {path}")
    return found


def quaternion_yaw(rotation) -> float:
    w, x, y, z = [float(value) for value in rotation]
    return math.atan2(2.0 * (w * z + x * y), 1.0 - 2.0 * (y * y + z * z))


def recover_global_context(cases: pd.DataFrame) -> pd.DataFrame:
    sensors = load_small_json("sensor.json")
    lidar_sensors = {record["token"] for record in sensors if record.get("channel") == "LIDAR_TOP"}
    if not lidar_sensors:
        raise AssertionError("No LIDAR_TOP sensor metadata")
    calibrated = load_small_json("calibrated_sensor.json")
    lidar_calibrated = {record["token"] for record in calibrated if record.get("sensor_token") in lidar_sensors}
    wanted_samples = set(cases.sample_token.astype(str))
    sample_data = stream_json_records(
        META_ROOT / "sample_data.json",
        lambda record: record.get("sample_token") in wanted_samples
        and record.get("calibrated_sensor_token") in lidar_calibrated
        and bool(record.get("is_key_frame")),
        len(wanted_samples),
    )
    by_sample = {record["sample_token"]: record for record in sample_data}
    if len(by_sample) != len(wanted_samples):
        raise AssertionError("Multiple/missing LIDAR_TOP keyframes for selected samples")
    wanted_poses = {record["ego_pose_token"] for record in sample_data}
    poses = stream_json_records(
        META_ROOT / "ego_pose.json",
        lambda record: record.get("token") in wanted_poses,
        len(wanted_poses),
    )
    pose_by_token = {record["token"]: record for record in poses}
    scenes = {record["token"]: record for record in load_small_json("scene.json")}
    logs = {record["token"]: record for record in load_small_json("log.json")}
    maps = load_small_json("map.json")
    map_by_log: dict[str, dict] = {}
    for record in maps:
        for log_token in record.get("log_tokens", []):
            if log_token in map_by_log:
                raise AssertionError(f"Log token appears in multiple map records: {log_token}")
            map_by_log[log_token] = record
    rows: list[dict[str, object]] = []
    for _, row in cases.iterrows():
        sample_token = str(row.sample_token)
        scene_token = str(row.scene_token)
        scene = scenes[scene_token]
        if str(scene["log_token"]) != str(row.log_token):
            raise AssertionError(f"Scene/log mismatch for panel {row.panel}")
        log = logs[scene["log_token"]]
        map_record = map_by_log.get(scene["log_token"])
        if map_record is None:
            raise AssertionError(f"No map record for log {scene['log_token']}")
        sd = by_sample[sample_token]
        pose = pose_by_token[sd["ego_pose_token"]]
        rows.append(
            {
                "map_location": str(log.get("location", "")),
                "map_token": str(map_record["token"]),
                "map_filename": str(map_record["filename"]),
                "ego_global_x": float(pose["translation"][0]),
                "ego_global_y": float(pose["translation"][1]),
                "ego_global_yaw": quaternion_yaw(pose["rotation"]),
                "ego_pose_token": str(pose["token"]),
                "lidar_top_sample_data_token": str(sd["token"]),
            }
        )
    return pd.concat([cases.reset_index(drop=True), pd.DataFrame(rows)], axis=1)


def extract_official_maps(map_tokens: set[str]) -> dict[str, Path]:
    destination = OUTPUT / "official_map_assets"
    destination.mkdir(parents=True, exist_ok=True)
    members = {f"maps/{token}.png": token for token in map_tokens}
    result: dict[str, Path] = {}
    with tarfile.open(ARGS.map_archive, "r:gz") as archive:
        available = {member.name: member for member in archive.getmembers()}
        missing = sorted(set(members) - set(available))
        if missing:
            raise FileNotFoundError("MAP_ASSET_NOT_FOUND: " + ", ".join(missing))
        for member_name, token in members.items():
            output_path = destination / f"{token}.png"
            if not output_path.exists():
                source = archive.extractfile(available[member_name])
                if source is None:
                    raise FileNotFoundError(f"MAP_ASSET_NOT_FOUND: {member_name}")
                output_path.write_bytes(source.read())
            result[token] = output_path
    return result


def common_extent(arrays: dict[str, np.ndarray]) -> tuple[float, float, float, float]:
    all_points = np.concatenate([arrays[name].reshape(-1, 2) for name in arrays], axis=0)
    longitudinal_min = min(-10.0, float(all_points[:, 0].min()) - 2.0)
    longitudinal_max = max(25.0, float(all_points[:, 0].max()) + 4.0)
    lateral_half = max(12.0, float(np.abs(all_points[:, 1]).max()) + 3.0)
    return (-lateral_half, lateral_half, longitudinal_min, longitudinal_max)


def crop_map_to_local(
    map_path: Path,
    anchor_x: float,
    anchor_y: float,
    yaw: float,
    extent: tuple[float, float, float, float],
    output_path: Path,
    width: int = 900,
    height: int = 900,
) -> None:
    lateral_min, lateral_max, longitudinal_min, longitudinal_max = extent
    with Image.open(map_path) as source:
        source = source.convert("L")
        source_width, source_height = source.size
        resolution = 0.1
        c, s = math.cos(yaw), math.sin(yaw)
        dly_du = (lateral_max - lateral_min) / (width - 1)
        dlx_dv = -(longitudinal_max - longitudinal_min) / (height - 1)
        lx_at_zero = longitudinal_max
        ly_at_zero = lateral_min
        # local (forward x, left y) -> global, then global metres -> nuScenes map pixels.
        a = (-s * dly_du) / resolution
        b = (c * dlx_dv) / resolution
        c0 = (anchor_x + c * lx_at_zero - s * ly_at_zero) / resolution
        d = (-c * dly_du) / resolution
        e = (-s * dlx_dv) / resolution
        f0 = source_height - (anchor_y + s * lx_at_zero + c * ly_at_zero) / resolution
        sampled = source.transform(
            (width, height),
            Image.Transform.AFFINE,
            (a, b, c0, d, e, f0),
            resample=Image.Resampling.BILINEAR,
            fillcolor=0,
        )
        mask = np.asarray(sampled, dtype=np.uint8)
    # Official semantic prior only: preserve foreground geometry, use a quiet paper palette.
    foreground = mask > 127
    rgb = np.empty((height, width, 3), dtype=np.uint8)
    rgb[:] = np.array([250, 250, 250], dtype=np.uint8)
    rgb[foreground] = np.array([235, 237, 239], dtype=np.uint8)
    Image.fromarray(rgb, mode="RGB").save(output_path)


def local_to_global(points: np.ndarray, x: float, y: float, yaw: float) -> np.ndarray:
    c, s = math.cos(yaw), math.sin(yaw)
    result = np.empty_like(points, dtype=float)
    result[:, 0] = x + c * points[:, 0] - s * points[:, 1]
    result[:, 1] = y + s * points[:, 0] + c * points[:, 1]
    return result


def make_debug_alignment(cases: pd.DataFrame, arrays: dict[str, np.ndarray], map_paths: dict[str, Path]) -> None:
    for i, row in cases.iterrows():
        gt_global = local_to_global(
            arrays["gt"][i], float(row.ego_global_x), float(row.ego_global_y), float(row.ego_global_yaw)
        )
        hist_global = local_to_global(
            arrays["history"][i], float(row.ego_global_x), float(row.ego_global_y), float(row.ego_global_yaw)
        )
        points = np.vstack([gt_global, hist_global])
        margin = 8.0
        xmin, xmax = float(points[:, 0].min() - margin), float(points[:, 0].max() + margin)
        ymin, ymax = float(points[:, 1].min() - margin), float(points[:, 1].max() + margin)
        with Image.open(map_paths[str(row.map_token)]) as image:
            image = image.convert("L")
            w, h = image.size
            res = 0.1
            left = max(0, int(math.floor(xmin / res)))
            right = min(w, int(math.ceil(xmax / res)))
            top = max(0, int(math.floor(h - ymax / res)))
            bottom = min(h, int(math.ceil(h - ymin / res)))
            crop = np.asarray(image.crop((left, top, right, bottom)))
            extent = (left * res, right * res, (h - bottom) * res, (h - top) * res)
        fig, ax = plt.subplots(figsize=(5.0, 5.0), dpi=180)
        ax.imshow(crop, cmap="gray", origin="upper", extent=extent, alpha=0.42)
        ax.plot(hist_global[:, 0], hist_global[:, 1], "o-", color="#59636F", lw=1.2, ms=3, label="History")
        ax.plot(gt_global[:, 0], gt_global[:, 1], "-", color="#20262E", lw=1.6, label="GT")
        ax.scatter([row.ego_global_x], [row.ego_global_y], c="#C62828", s=25, label="Anchor")
        arrow_len = 5.0
        ax.arrow(
            row.ego_global_x,
            row.ego_global_y,
            arrow_len * math.cos(row.ego_global_yaw),
            arrow_len * math.sin(row.ego_global_yaw),
            width=0.08,
            color="#C62828",
            length_includes_head=True,
        )
        ax.set_aspect("equal")
        ax.set_xlabel("Global x (m)")
        ax.set_ylabel("Global y (m)")
        ax.set_title(f"Panel ({row.panel}) map alignment: {row.map_location}")
        ax.legend(fontsize=8)
        fig.tight_layout()
        fig.savefig(OUTPUT / f"debug_{row.panel}_map_alignment.png", dpi=220)
        plt.close(fig)


def format_delta(value_m: float) -> str:
    return f"{value_m * 1000:+.1f} mm".replace("+", "+").replace("-", "−")


def make_final_figure(
    cases: pd.DataFrame,
    arrays: dict[str, np.ndarray],
    extent: tuple[float, float, float, float],
    map_crop_paths: list[Path],
) -> None:
    colors = {"history": "#59636F", "gt": "#20262E", "raw": "#59636F", "fixed": "#2F7FB3", "selected": "#E49A3A"}
    fig, axes = plt.subplots(2, 2, figsize=(178 / 25.4, 170 / 25.4), dpi=400)
    plt.subplots_adjust(left=0.075, right=0.985, top=0.90, bottom=0.10, wspace=0.18, hspace=0.42)
    lateral_min, lateral_max, longitudinal_min, longitudinal_max = extent
    for i, (ax, (_, row), map_crop_path) in enumerate(zip(axes.flat, cases.iterrows(), map_crop_paths)):
        ax.imshow(
            Image.open(map_crop_path),
            extent=(lateral_min, lateral_max, longitudinal_min, longitudinal_max),
            origin="upper",
            interpolation="bilinear",
            zorder=0,
        )
        # Display lateral on the horizontal axis and forward longitudinal on the vertical axis.
        ax.plot(arrays["history"][i, :, 1], arrays["history"][i, :, 0], color=colors["history"], lw=1.0, marker="o", ms=3.2, mfc="white", mew=0.8, zorder=4)
        ax.plot(arrays["gt"][i, :, 1], arrays["gt"][i, :, 0], color=colors["gt"], lw=1.3, zorder=5)
        ax.plot(arrays["raw"][i, :, 1], arrays["raw"][i, :, 0], color=colors["raw"], lw=1.05, marker="o", ms=3.3, mfc="white", mew=0.8, zorder=6)
        ax.plot(arrays["fixed"][i, :, 1], arrays["fixed"][i, :, 0], color=colors["fixed"], lw=1.05, marker="s", ms=3.2, mfc="white", mew=0.8, zorder=7)
        ax.plot(arrays["selected"][i, :, 1], arrays["selected"][i, :, 0], color=colors["selected"], lw=1.05, marker="D", ms=3.0, mfc="white", mew=0.8, zorder=8)
        ax.scatter([0], [0], s=9, c="#20262E", zorder=9)
        comparison = "SF" if row.panel == "d" else "FR"
        comparison_label = "Sel. − SG" if row.panel == "d" else "SG − Raw"
        metric_text = (
            f"{comparison_label}\n"
            f"ΔADE {format_delta(float(row[f'delta_ade_{comparison}']))}\n"
            f"ΔFDE {format_delta(float(row[f'delta_fde_{comparison}']))}\n"
            f"ΔShape {float(row[f'delta_shape_{comparison}']):+.2f} m s$^{{-3}}$".replace("-", "−")
        )
        ax.text(
            0.025,
            0.97,
            metric_text,
            transform=ax.transAxes,
            va="top",
            ha="left",
            fontsize=8,
            linespacing=1.12,
            bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.78, "pad": 1.6},
            zorder=12,
        )
        wrapped_title = {
            "a": "Typical geometry\nreduction",
            "b": "Accuracy preserved,\ngeometry altered",
            "c": "Local error\nincrease",
            "d": "Selected differs from\nFixed SG",
        }[str(row.panel)]
        ax.text(0.0, 1.155, f"({row.panel})", transform=ax.transAxes, fontsize=10, fontweight="bold", ha="left", va="top", clip_on=False)
        ax.text(0.22, 1.155, wrapped_title, transform=ax.transAxes, fontsize=9, fontweight="bold", ha="left", va="top", linespacing=1.0, clip_on=False)
        ax.text(0.22, 1.050, str(row.panel_note), transform=ax.transAxes, fontsize=8, fontstyle="italic", ha="left", va="top", color="#454B52", clip_on=False)
        ax.set_xlim(lateral_min, lateral_max)
        ax.set_ylim(longitudinal_min, longitudinal_max)
        ax.set_aspect("equal", adjustable="box")
        ax.set_xlabel("Lateral (m)", fontsize=8)
        ax.set_ylabel("Longitudinal (m)", fontsize=8)
        ax.tick_params(labelsize=8, length=2.5, width=0.5, colors="#454B52")
        for spine in ax.spines.values():
            spine.set_color("#C7CCD1")
            spine.set_linewidth(0.55)
    handles = [
        Line2D([0], [0], color=colors["history"], lw=1.0, marker="o", ms=4, mfc="white", label="History"),
        Line2D([0], [0], color=colors["gt"], lw=1.3, label="GT"),
        Line2D([0], [0], color=colors["raw"], lw=1.05, marker="o", ms=4, mfc="white", label="Raw"),
        Line2D([0], [0], color=colors["fixed"], lw=1.05, marker="s", ms=4, mfc="white", label="Fixed SG"),
        Line2D([0], [0], color=colors["selected"], lw=1.05, marker="D", ms=4, mfc="white", label="Selected"),
    ]
    fig.legend(handles=handles, loc="lower center", bbox_to_anchor=(0.5, 0.018), ncol=5, frameon=False, fontsize=8.5, handlelength=2.3, columnspacing=1.4)
    fig.savefig(OUTPUT / "Fig03_qualitative_real_bev.png", dpi=500, facecolor="white")
    fig.savefig(OUTPUT / "Fig03_qualitative_real_bev.pdf", facecolor="white")
    fig.savefig(OUTPUT / "Fig03_qualitative_real_bev.svg", facecolor="white")
    plt.close(fig)


def export_tables_and_payload(
    cases: pd.DataFrame,
    arrays: dict[str, np.ndarray],
    extent: tuple[float, float, float, float],
    map_crop_paths: list[Path],
    reference_audit: dict,
    selection_audit: dict,
) -> None:
    cases = cases.copy()
    rename = {
        f"ade__{STRATEGY_RAW}": "ADE_raw",
        f"ade__{STRATEGY_FIXED}": "ADE_fixed",
        f"ade__{STRATEGY_SELECTED}": "ADE_selected",
        f"fde__{STRATEGY_RAW}": "FDE_raw",
        f"fde__{STRATEGY_FIXED}": "FDE_fixed",
        f"fde__{STRATEGY_SELECTED}": "FDE_selected",
        f"history_aware_mean_jerk__{STRATEGY_RAW}": "Shape_raw",
        f"history_aware_mean_jerk__{STRATEGY_FIXED}": "Shape_fixed",
        f"history_aware_mean_jerk__{STRATEGY_SELECTED}": "Shape_selected",
    }
    cases = cases.rename(columns=rename)
    desired = [
        "panel", "panel_title", "panel_note", "run_id", "model", "seed", "selected_smoother",
        "scene_token", "sample_token", "window_index", "log_token", "map_location",
        "ego_global_x", "ego_global_y", "ego_global_yaw", "map_token",
        "ADE_raw", "ADE_fixed", "ADE_selected", "FDE_raw", "FDE_fixed", "FDE_selected",
        "Shape_raw", "Shape_fixed", "Shape_selected",
        "delta_ade_FR", "delta_fde_FR", "delta_shape_FR",
        "delta_ade_SF", "delta_fde_SF", "delta_shape_SF",
    ]
    missing = [column for column in desired if column not in cases.columns]
    if missing:
        raise KeyError(f"Selected-case export columns missing: {missing}")
    cases[desired].to_csv(OUTPUT / "Fig03_case_selection.csv", index=False)
    cases[desired].to_csv(OUTPUT / "fig3_selected_cases.csv", index=False)
    debug_cols = [
        "panel", "run_id", "scene_token", "sample_token", "window_index", "log_token",
        "map_location", "map_token", "ego_global_x", "ego_global_y", "ego_global_yaw",
        "ego_pose_token", "lidar_top_sample_data_token",
    ]
    cases[debug_cols].to_csv(OUTPUT / "Fig03_debug_keys.csv", index=False)
    np.savez_compressed(
        OUTPUT / "fig3_selected_trajectories.npz",
        history_xy=arrays["history"],
        future_xy=arrays["gt"],
        raw_prediction=arrays["raw"],
        fixed_sg_prediction=arrays["fixed"],
        selected_prediction=arrays["selected"],
        panel=np.asarray(cases.panel.astype(str).tolist(), dtype="U"),
        run_id=np.asarray(cases.run_id.astype(str).tolist(), dtype="U"),
        scene_token=np.asarray(cases.scene_token.astype(str).tolist(), dtype="U"),
        sample_token=np.asarray(cases.sample_token.astype(str).tolist(), dtype="U"),
        window_index=cases.window_index.astype(int).to_numpy(),
        log_token=np.asarray(cases.log_token.astype(str).tolist(), dtype="U"),
        map_location=np.asarray(cases.map_location.astype(str).tolist(), dtype="U"),
    )
    summary = {
        "status": "REAL_BEV_GENERATED_FROM_OFFICIAL_NUSCENES_SEMANTIC_PRIOR",
        "manual_override": False,
        "data_scope": {"test_windows": 2901, "test_scenes": 93, "test_logs": 7, "formal_runs": 50},
        "primary_key": ["run_id", "scene_token", "sample_token"],
        "coordinate_convention": {
            "stored": "ego-centric local; x forward, y left; final history point at origin",
            "display": "horizontal=lateral y, vertical=longitudinal x",
            "map_transform": "global = anchor_translation + R(anchor_yaw) @ local",
        },
        "map_source": {
            "archive": str(ARGS.map_archive),
            "asset_type": "official nuScenes semantic-prior raster",
            "resolution_m_per_pixel": 0.1,
            "expansion_lane_layers_available": False,
            "surrounding_agent_annotations_available": False,
            "note": "No lane or agent geometry was invented; only the official semantic prior is shown.",
        },
        "reference_run": reference_audit,
        "case_selection": selection_audit,
        "selected_windows": cases[debug_cols].to_dict(orient="records"),
        "common_extent": {
            "lateral_min": extent[0], "lateral_max": extent[1],
            "longitudinal_min": extent[2], "longitudinal_max": extent[3],
        },
        "map_crop_files": [str(path) for path in map_crop_paths],
        "metric_QA": "ADE/FDE recomputed from frozen trajectories and matched parquet within 1e-5; Shape uses authoritative parquet values.",
    }
    (OUTPUT / "fig3_selection_summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    ppt_payload = {
        "slide": {"width": 672.7559, "height": 642.5197},
        "extent": summary["common_extent"],
        "cases": [],
    }
    for i, row in cases.iterrows():
        comparison = "SF" if row.panel == "d" else "FR"
        ppt_payload["cases"].append(
            {
                "panel": row.panel,
                "title": row.panel_title,
                "note": row.panel_note,
                "comparison": "Sel. - SG" if row.panel == "d" else "SG - Raw",
                "delta_ade_mm": float(row[f"delta_ade_{comparison}"]) * 1000,
                "delta_fde_mm": float(row[f"delta_fde_{comparison}"]) * 1000,
                "delta_shape": float(row[f"delta_shape_{comparison}"]),
                "map_crop": str(map_crop_paths[i]),
                "history": arrays["history"][i].tolist(),
                "gt": arrays["gt"][i].tolist(),
                "raw": arrays["raw"][i].tolist(),
                "fixed": arrays["fixed"][i].tolist(),
                "selected": arrays["selected"][i].tolist(),
            }
        )
    (OUTPUT / "fig3_ppt_payload.json").write_text(json.dumps(ppt_payload, indent=2), encoding="utf-8")


def main() -> None:
    require_paths()
    OUTPUT.mkdir(parents=True, exist_ok=True)
    with np.load(PAYLOAD_PATH, allow_pickle=False) as payload:
        print("heldout keys:", payload.files)
        for key in payload.files:
            print(key, payload[key].shape, payload[key].dtype)
        assert payload["history_xy"].shape == (2901, 4, 2)
        assert payload["future_xy"].shape == (2901, 6, 2)
        assert len(np.unique(payload["scene_token"])) == 93
        assert len(np.unique(payload["log_token"])) == 7
    provenance = pd.read_parquet(PROVENANCE_PATH)
    if len(provenance) != 2901 or provenance.duplicated(["scene_token", "anchor_sample_token"]).any():
        raise AssertionError("Provenance row count or composite uniqueness failed")
    metrics = pd.read_parquet(METRICS_PATH)
    wide = add_effect_columns(validate_and_pivot_metrics(metrics))
    smoother_df = load_selected_smoothers(sorted(wide.run_id.unique().tolist()))
    ranking, reference_audit = rank_reference_runs(wide, smoother_df)
    reference = reference_audit["selected"]
    run_id = str(reference["run_id"])
    selected_smoother = str(reference["selected_smoother"])
    run_wide = wide[wide.run_id == run_id].merge(
        smoother_df[["run_id", "selected_smoother"]], on="run_id", validate="many_to_one"
    )
    if len(run_wide) != 2901:
        raise AssertionError("Reference run does not have exactly 2901 windows")
    cases, selection_audit = select_cases(run_wide, selected_smoother)
    cases, arrays = attach_trajectories_and_recompute(cases, run_id)
    cases = recover_global_context(cases)
    map_paths = extract_official_maps(set(cases.map_token.astype(str)))
    extent = common_extent(arrays)
    crop_dir = OUTPUT / "map_crops"
    crop_dir.mkdir(exist_ok=True)
    map_crop_paths: list[Path] = []
    for _, row in cases.iterrows():
        crop_path = crop_dir / f"panel_{row.panel}_{row.sample_token}.png"
        crop_map_to_local(
            map_paths[str(row.map_token)],
            float(row.ego_global_x),
            float(row.ego_global_y),
            float(row.ego_global_yaw),
            extent,
            crop_path,
        )
        map_crop_paths.append(crop_path)
    make_debug_alignment(cases, arrays, map_paths)
    make_final_figure(cases, arrays, extent, map_crop_paths)
    export_tables_and_payload(cases, arrays, extent, map_crop_paths, reference_audit, selection_audit)
    print("REFERENCE_RUN", run_id, reference["model"], int(reference["seed"]), selected_smoother)
    print(cases[["panel", "scene_token", "sample_token", "window_index", "map_location", "delta_ade_FR", "delta_fde_FR", "delta_shape_FR", "delta_ade_SF", "delta_fde_SF", "delta_shape_SF"]].to_string(index=False))
    print("OUTPUT", OUTPUT)


if __name__ == "__main__":
    main()
