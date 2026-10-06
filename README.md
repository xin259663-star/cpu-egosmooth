# Anonymous manuscript reproduction repository

**Paper:** Measurement and Verification of Post-Processing Effects in Short-Horizon Ego-Trajectory Prediction for Autonomous Driving

**Status:** Anonymous manuscript reproduction repository

This repository contains the frozen scientific sources, provenance records, and locked publication artwork for anonymous review. The current main figures are `figures/Fig01_final.svg` through `figures/Fig06_final.svg`; Supplementary Figures S07 and S08 are also in `figures/`. The publication SVGs are locked artwork. The reproduction command validates their hashes and the frozen scientific-source hashes, then exports exact copies. It does not retrain models, recompute results, or reselect qualitative cases.

## Current manuscript mapping

| Item | Content |
| --- | --- |
| Fig. 1 | Development and held-out Test workflow |
| Fig. 2 | Ego-window construction, log-exclusive split, and role isolation |
| Fig. 3 | Four deterministic held-out trajectory cases |
| Fig. 4 | Paired post-processing effects |
| Fig. 5 | Local paired-error and boundary/endpoint effects |
| Fig. 6 | Selected-candidate composition and rule sensitivity |
| Table 5 | Timing-definition sensitivity (`analysis/Table05_source.csv`) |
| Table 6 | Kinematic controls (`analysis/Table06_source.csv`) |
| Fig. S07 | Supplementary sensitivity diagnostics |
| Fig. S08 | Predictor-stratified paired effects |

## Reproduction

```bash
python scripts/reproduce_figures.py --root . --fig all --output reproduced_figures
python scripts/reproduce_publication_tables.py --root .
pytest -q
```

The held-out cases and deterministic selection rules are documented in `results/provenance/`. The frozen Fig. 3(b) case is scene `b0b26c1e5a1140e69598422f12ae1dc0`, sample `53a3b6ba49af484d9d0bab0ffb9dea01`, log `7a0fde44c3504eaeb18f9ad83bed65bc`, window `19`.

Map context is used only for qualitative visualization and is not provided to predictors, post-processing, candidate selection, or quantitative evaluation. The licensed raw dataset is not redistributed.

`manifest_current.json` identifies the current output set and records SHA-256 hashes for Fig. 1-Fig. 6, Fig. S07, Fig. S08, Table 5, Table 6, and frozen scientific sources. Superseded publication manifests and artwork are retained only under `figures/archive/` and are not current outputs.

## Repository structure

- `src/`: scientific implementation
- `scripts/`: reproduction and validation entry points
- `configs/`: frozen experimental configuration
- `analysis/`: audited supplementary analyses and table sources
- `results/`: processed summaries, tables, and provenance
- `figures/`: current locked publication artwork
- `figures/archive/`: superseded artwork and manifests

## Scientific scope

The study evaluates short-horizon open-loop ego-trajectory post-processing. It separates displacement accuracy, sampled-path geometry, local paired effects, and selection sensitivity. It does not claim improved safety, comfort, physical jerk, closed-loop behavior, or complete autonomous-driving performance.
