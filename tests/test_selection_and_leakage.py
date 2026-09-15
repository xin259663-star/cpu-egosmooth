
from pathlib import Path
import pandas as pd
from egosmooth.selection import select_validation_b_candidate

def test_gate_precedes_lexicographic_rank():
    frame=pd.DataFrame([
        {"id":"infeasible_low_shape","delta_ade":0.01,"delta_fde":0.0,"history_aware_mean_jerk":0.0,"ade":0.0,"fde":0.0,"enumeration_order":0},
        {"id":"feasible","delta_ade":0.0,"delta_fde":-0.01,"history_aware_mean_jerk":1.0,"ade":1.0,"fde":1.0,"enumeration_order":1},
    ])
    assert select_validation_b_candidate(frame)["id"]=="feasible"

def test_test_is_final_evaluation_only():
    text=Path("configs/experiment/protocol.yaml").read_text(encoding="utf-8")
    assert "development_use: false" in text
    assert "purpose: postprocessing_selection" in text
