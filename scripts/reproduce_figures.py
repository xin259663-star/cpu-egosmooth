
from __future__ import annotations
import argparse
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def _save(fig, root, n):
    out = root / "figures/reproduced"
    out.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(out / f"Fig{n:02d}.png", dpi=220)
    fig.savefig(out / f"Fig{n:02d}.pdf")
    plt.close(fig)

def reproduce(n, root):
    d = root / "results/figure_data"
    if n == 4:
        f = pd.read_csv(d / "fig04_aux_geometry_effects.csv")
        f = f[f.metric.isin(["mean_geometric_acceleration", "integrated_squared_acceleration", "mean_abs_curvature"])]
        p = f.pivot(index="metric_label", columns="comparison", values="mean_paired_difference")
        label_map={"Integrated squared acceleration":"Integrated squared\nacceleration","Mean absolute curvature":"Mean absolute\ncurvature","Mean geometric acceleration":"Mean geometric\nacceleration"}; p.index=[label_map.get(x,x) for x in p.index]
        ax = p.plot.bar(figsize=(9.5, 4.8), color=["#4778a8", "#d17a3f", "#6b9f78"]); ax.axhline(0, color="black", lw=.8); ax.set_xlabel(""); ax.set_ylabel("Mean paired difference"); ax.set_title("Auxiliary sampled-geometry effects"); ax.tick_params(axis="x", rotation=0); ax.legend(fontsize=7, loc="lower right")
        _save(ax.figure, root, n)
    elif n == 5:
        f = pd.read_csv(d / "fig05_threshold_summary.csv")
        fig, ax = plt.subplots(figsize=(8, 4.5))
        for (comp, metric), g in f.groupby(["comparison", "metric"]):
            ax.plot(g.threshold_mm, 100*g.exceed_rate, marker="o", label=f"{comp}; {metric}")
        ax.set(xlabel="Descriptive threshold (mm)", ylabel="Positive-change rate (%)", title="Local paired-error threshold sensitivity"); ax.legend(fontsize=7)
        _save(fig, root, n)
    elif n == 6:
        f = pd.read_csv(d / "fig06_case_metrics.csv")
        g = f[f.metric.isin(["ade", "fde"])].copy(); g["estimate_mm"] = 1000*g.estimate
        p = g.groupby(["label", "comparison"], as_index=False).estimate_mm.mean().pivot(index="label", columns="comparison", values="estimate_mm")
        labels={"accelerating":"Accelerating","decelerating":"Decelerating","high":"High speed","high_history_curvature":"High hist. curvature","stationary_or_very_low":"Very low speed","straight":"Straight","turning":"Turning"}; p.index=[labels.get(x,x) for x in p.index]
        ax = p.plot.bar(figsize=(9.5, 4.8), color=["#4778a8", "#d17a3f"]); ax.axhline(0, color="black", lw=.8); ax.set_xlabel(""); ax.set_ylabel("Mean paired difference (mm)"); ax.set_title("Deterministically selected qualitative-case effects"); ax.tick_params(axis="x", rotation=25); ax.legend(fontsize=7)
        _save(ax.figure, root, n)
    elif n == 7:
        f = pd.read_csv(d / "fig07_timestamp_sensitivity.csv")
        fig, ax = plt.subplots(figsize=(8, 4.5))
        for comp, g in f.groupby("comparison"):
            ax.bar(np.arange(len(g)) + (0 if "Fixed" in comp else .35), g.relative_reduction_percent, width=.35, label=comp)
        ax.set_xticks([.175, 1.175], ["Nominal grid", "Exact timestamps"]); ax.set_ylabel("Shape reduction (%)"); ax.set_title("Shape-definition sensitivity"); ax.legend(fontsize=8)
        _save(fig, root, n)
    elif n == 8:
        f = pd.read_csv(d / "fig08_kinematic_controls.csv"); f=f[f.strategy=="Raw"]
        neural=f[f.method_type=="neural"].copy(); controls=f[f.method_type=="kinematic baseline"].copy()
        fig, axes = plt.subplots(1,3,figsize=(12.5,4.2)); specs=[("ADE","ADE (m)"),("FDE","FDE (m)"),("history_aware_mean_geometric_jerk","Shape (m s$^{-3}$)")]
        x1=np.arange(len(controls)); x2=np.arange(len(neural))+len(controls)+1
        for ax,(col,label) in zip(axes,specs):
            ax.scatter(x1,controls[col],marker="D",s=55,color="#4778a8",label="Kinematic control"); ax.scatter(x2,neural[col],s=45,color="#d17a3f",label="Neural Raw")
            ax.set_xticks(np.r_[x1,x2]); ax.set_xticklabels(list(controls.method)+["Neural\nmean" if x=="Neural overall" else ("Pos-Tr." if x=="PositionalTransformer" else x) for x in neural.method],rotation=45,ha="right",fontsize=7); ax.set_ylabel(label); ax.grid(axis="y",alpha=.2)
        axes[0].legend(fontsize=7); fig.suptitle("Kinematic controls and the Shape interpretation boundary")
        _save(fig, root, n)
    else:
        raise ValueError("Processed-data regeneration is implemented for Figures 4-8")

def main():
    p=argparse.ArgumentParser(); p.add_argument("--fig", default="all"); p.add_argument("--root", type=Path, default=Path(".")); a=p.parse_args()
    nums=range(4,9) if a.fig=="all" else [int(a.fig)]
    for n in nums: reproduce(n,a.root)
if __name__ == "__main__": main()
