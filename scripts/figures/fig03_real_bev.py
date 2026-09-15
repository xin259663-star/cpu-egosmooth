
from __future__ import annotations
import argparse
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

def trajectory_only(npz_path: Path, output: Path) -> None:
    data = np.load(npz_path, allow_pickle=False)
    required = ["history_xy", "future_xy", "raw_prediction", "fixed_sg_prediction", "selected_prediction", "panel"]
    missing = [key for key in required if key not in data]
    if missing:
        raise ValueError(f"trajectory NPZ is missing fields: {missing}")
    fig, axes = plt.subplots(1, 4, figsize=(12, 3.4))
    for index, ax in enumerate(axes):
        for values, label, style in [(data["history_xy"][index], "History", "k.-"), (data["future_xy"][index], "GT", "g.-"), (data["raw_prediction"][index], "Raw", "C0.--"), (data["fixed_sg_prediction"][index], "Fixed SG(5,2)", "C1.-"), (data["selected_prediction"][index], "Selected", "C3.-")]:
            ax.plot(values[:, 1], values[:, 0], style, label=label)
        ax.set_title(f"({data['panel'][index]})")
        ax.set_xlabel("Lateral (m)"); ax.set_ylabel("Longitudinal (m)"); ax.set_aspect("equal", adjustable="box"); ax.grid(alpha=.2)
    handles, labels = axes[0].get_legend_handles_labels(); fig.legend(handles, labels, loc="upper center", ncol=5); fig.tight_layout(rect=(0,0,1,.88))
    output.parent.mkdir(parents=True, exist_ok=True); fig.savefig(output, dpi=240); plt.close(fig)

def main() -> int:
    parser = argparse.ArgumentParser(description="Render the formal four-case Figure 3 from reviewed local assets.")
    parser.add_argument("--trajectory-npz", type=Path)
    parser.add_argument("--nuscenes-root", type=Path)
    parser.add_argument("--output", type=Path, default=Path("figures/reproduced/Fig03_trajectory_only.png"))
    args = parser.parse_args()
    if args.trajectory_npz is None or not args.trajectory_npz.is_file():
        print("nuScenes data/map and the reviewed selected-trajectory NPZ are required for Fig.3 BEV reconstruction.")
        print("These third-party/derived assets are intentionally not redistributed; see docs/FIGURE3_PROVENANCE.md.")
        return 0
    trajectory_only(args.trajectory_npz, args.output)
    if args.nuscenes_root is None or not args.nuscenes_root.exists():
        print(f"Trajectory-only Figure 3 written to {args.output}.")
        print("A local nuScenes installation is required for the official semantic-prior BEV background.")
    else:
        print(f"Trajectory-only Figure 3 written to {args.output}; use the documented internal provenance to add the local nuScenes map background.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
