
# Reproducibility

## Level 1: processed results to tables and figures

**Status: VERIFIED.** A clean Python 3.11 environment reproduces processed-result tables and Figures 4-8 without nuScenes or private project paths.

```bash
python scripts/reproduce_tables.py --results-root results
python scripts/reproduce_figures.py --fig all
pytest -q
```

## Level 2: saved predictions to metrics/results

**Status: VERIFIED INTERNALLY; NOT SELF-CONTAINED HERE.** Frozen saved predictions were used in the audited Phase 1-7 recomputation, including ADE/FDE checks. Complete predictions are not redistributed in this compact repository. A future external archive is described in `ARCHIVAL_DATA_PLAN.md`.

## Level 3: raw nuScenes through final held-out evaluation

**Status: PARTIALLY DOCUMENTED / REVIEW GATE.** This level requires official nuScenes data, log-exclusive preprocessing, normalization from Training only, predictor training, Validation-A checkpoint selection, Raw prediction, Validation-B post-processing selection, and one final held-out Test evaluation. The scientific definitions and configurations are public, but internal environment orchestration has not passed a fresh-machine end-to-end release test.

Test is never used for training, checkpoint selection, candidate selection, or hyperparameter selection.

## Figure 3

The repository intentionally excludes the trajectory NPZ and raw nuScenes map assets. Without reviewed saved trajectories, `scripts/figures/fig03_real_bev.py` prints the required inputs and exits cleanly. With a reviewed trajectory NPZ it can generate a trajectory-only rendering; the official BEV background additionally requires a local nuScenes installation.
