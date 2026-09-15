
from pathlib import Path
import json
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
runs=pd.read_csv(ROOT/"results/summary/formal_runs_summary.csv")
index=pd.read_csv(ROOT/"results/provenance/test_window_index.csv")
protocol=(ROOT/"configs/experiment/protocol.yaml").read_text(encoding="utf-8")
assert len(runs)==50 and runs.model.nunique()==5 and set(runs.seed)==set(range(10))
assert len(index)==2901 and index.scene_token.nunique()==93 and index.log_token.nunique()==7
assert not index.duplicated(["scene_token","sample_token"]).any()
for term in ["history_steps: 4","future_steps: 6","nominal_dt_seconds: 0.5","primary_candidate_epsilon: 0.0","sg_w5_p2","validation_b"]: assert term in protocol
fig3=json.loads((ROOT/"results/provenance/fig3_selection_summary.json").read_text(encoding="utf-8"))
assert fig3["manual_override"] is False and len(fig3["selected_windows"])==4
selected=fig3["reference_run"]["selected"]
assert selected["run_id"]=="P2B_042_log_primary_PositionalTransformer_s1" and selected["seed"]==1 and selected["selected_smoother"]=="qreg_l1"
print("scientific_consistency = PASS")
