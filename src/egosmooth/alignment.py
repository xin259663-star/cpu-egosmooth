
from __future__ import annotations
import pandas as pd

PUBLIC_KEY = ["run_id", "scene_token", "sample_token"]

def assert_unique_public_key(frame: pd.DataFrame) -> None:
    missing = [column for column in PUBLIC_KEY if column not in frame]
    if missing:
        raise KeyError(f"missing public-key columns: {missing}")
    if frame.duplicated(PUBLIC_KEY).any():
        raise ValueError("run_id + scene_token + sample_token is not unique")
