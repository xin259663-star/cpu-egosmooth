
# Data

## Third-party data

The study uses the publicly available nuScenes trainval release. The original dataset remains available through the official nuScenes source and is not redistributed here. Raw images, lidar sweeps, maps, complete annotation tables, and dataset archives are excluded. The repository provides compact log-split identifiers, derived supporting summaries, and code paths subject to the reproducibility levels documented in `REPRODUCIBILITY.md`.

## Derived inputs

The predictor input has shape `(N, 4, 5)` and the future target has shape `(N, 6, 2)` on a nominal 0.5 s grid. Split construction is log-exclusive. Complete derived tensors are not included in this repository.

## Prediction outputs

The evaluated strategies are Raw, Fixed SG(5,2), and Validation-B-selected. Complete prediction archives are not included in this repository.

## Figure 3

The provenance files identify the selected held-out windows, deterministic selection rules, run/model/seed, and metric values. The selected-trajectory NPZ, original map assets, sample annotations, and original metadata tables are not redistributed. Trajectory and map visualizations can be regenerated using the corresponding saved predictions and a local nuScenes installation.

## Metrics

ADE is mean Euclidean displacement error over six future points. FDE is final-point Euclidean error. Shape is the paper-facing name of the existing `history_aware_mean_jerk` implementation: a history-aware discrete third-difference descriptor formed from the last three historical positions and six predicted positions. Shape is not physical jerk and is not evidence of comfort, safety, feasibility, or closed-loop quality.

## Provenance keys

`window_index` is not globally unique. The cross-run key is `run_id + scene_token + sample_token`. Within one run, `scene_token + window_index` also locates a record. Never join records by `window_index` alone.
