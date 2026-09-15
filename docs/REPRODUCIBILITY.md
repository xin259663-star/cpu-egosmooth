
# Reproducibility

## Level 1: processed results to tables and figures

**Status: Verified.** A clean Python 3.11 environment reproduces the processed-result tables and Figures 4-8 without nuScenes or project-specific paths.

```bash
python scripts/reproduce_tables.py --results-root results
python scripts/reproduce_figures.py --fig all
pytest -q
```

## Level 2: saved predictions to metrics/results

**Status: Verified using the original saved predictions.** The reported metrics, including ADE and FDE, were recomputed from those predictions. Complete prediction files are not included in this repository.

## Level 3: raw nuScenes through final held-out evaluation

**Status: Partially documented.** This level requires official nuScenes data, log-exclusive preprocessing, normalization from Training only, predictor training, Validation-A checkpoint selection, Raw prediction, Validation-B post-processing selection, and one final held-out Test evaluation. The scientific definitions and configurations are included, but full end-to-end reproduction from raw nuScenes data requires additional environment setup and has not been validated as a self-contained fresh-machine workflow.

Test is never used for training, checkpoint selection, candidate selection, or hyperparameter selection.

## Figure 3

The repository does not include the trajectory NPZ or raw nuScenes map assets. Without the corresponding saved trajectories, `scripts/figures/fig03_real_bev.py` prints the required inputs and exits cleanly. With the trajectory NPZ, it can generate a trajectory-only rendering; the official BEV background additionally requires a local nuScenes installation.
