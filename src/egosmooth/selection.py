
from __future__ import annotations
import pandas as pd

RANK_COLUMNS = ["history_aware_mean_jerk", "ade", "fde", "enumeration_order"]

def select_validation_b_candidate(frame: pd.DataFrame) -> pd.Series:
    """Apply the frozen zero-tolerance gate, then lexicographic ranking."""
    required = {"delta_ade", "delta_fde", *RANK_COLUMNS}
    missing = sorted(required - set(frame.columns))
    if missing:
        raise KeyError(f"missing columns: {missing}")
    feasible = frame[(frame["delta_ade"] <= 0) & (frame["delta_fde"] <= 0)]
    if feasible.empty:
        raise ValueError("no feasible Validation-B candidate")
    return feasible.sort_values(RANK_COLUMNS, kind="mergesort").iloc[0]
