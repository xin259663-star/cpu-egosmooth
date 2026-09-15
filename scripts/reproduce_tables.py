
from __future__ import annotations
import argparse
from pathlib import Path
import pandas as pd

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--results-root", type=Path, default=Path("results"))
    args = p.parse_args()
    out = args.results_root / "tables/reproduced"
    out.mkdir(parents=True, exist_ok=True)
    runs = pd.read_csv(args.results_root / "summary/formal_runs_summary.csv")
    metrics = ["raw_ade", "raw_fde", "raw_history_aware_mean_jerk", "fixed_ade", "fixed_fde", "fixed_history_aware_mean_jerk", "selected_ade", "selected_fde", "selected_history_aware_mean_jerk"]
    runs[metrics].mean().rename("mean").to_csv(out / "formal_strategy_means.csv")
    effects = [c for c in runs if "_minus_" in c]
    runs[effects].agg(["mean", "std"]).T.to_csv(out / "formal_paired_effects.csv")
    print(out)
if __name__ == "__main__": main()
