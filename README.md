# Anonymous manuscript reproduction repository

**Paper:** Measurement and Verification of Post-Processing Effects in Short-Horizon Ego-Trajectory Prediction for Autonomous Driving

**Status:** Anonymous manuscript reproduction repository

This repository contains frozen scientific sources, provenance records, and locked publication artwork for anonymous review. The revised manuscript has five main figures, `figures/Fig01_final.svg` through `figures/Fig05_final.svg`. Supplementary Figure S07 is retained; the historical S08 artwork remains as a source record for the revised Supplementary Table S08. The reproduction command validates hashes and exports exact artwork copies. It does not retrain models, recompute results, or reselect qualitative cases.

## Current manuscript mapping

| Item | Content |
| --- | --- |
| Fig. 1 | Development and held-out Test workflow |
| Fig. 2 | Four deterministic held-out trajectory cases (historical Fig03) |
| Fig. 3 | Paired post-processing effects (historical Fig04) |
| Fig. 4 | Local paired-error and boundary/endpoint effects (historical Fig05) |
| Fig. 5 | Selected-candidate composition and rule sensitivity (historical Fig06) |
| Table 4 | Primary window-weighted strategy means |
| Table 5 | Kinematic controls (`results/tables/Table06_kinematic_controls.csv`, historical filename) |
| Fig. S07 | Supplementary sensitivity diagnostics |
| Table S08 | Predictor-stratified paired effects; historical FigS08 artwork retained as source |

## Reproduction

```bash
python scripts/reproduce_figures.py --root . --fig all --output reproduced_figures
python scripts/reproduce_publication_tables.py --root .
pytest -q
```

The held-out cases and deterministic selection rules are documented in `results/provenance/`. The frozen current Fig. 2(b), historically Fig. 3(b), is scene `b0b26c1e5a1140e69598422f12ae1dc0`, sample `53a3b6ba49af484d9d0bab0ffb9dea01`, log `7a0fde44c3504eaeb18f9ad83bed65bc`, window `19`.

Map context is used only for qualitative visualization and is not provided to predictors, post-processing, candidate selection, or quantitative evaluation. The licensed raw dataset is not redistributed.

`manifest_current.json` identifies the revised five-figure scope, the current Table 5 source, exact artwork hashes, and unchanged frozen scientific-source hashes. The prior six-figure state remains recoverable from Git commit `b062d14`; older journal-specific artwork is under `figures/archive/`. The historical Table05 timing and Table06 kinematic filenames are retained without renaming their scientific data.

See `docs/CURRENT_MANUSCRIPT_PROVENANCE.md` for current-to-historical file mapping, exact Test log identifiers, and the unresolved Train/Validation identifier gap. The repository supports source audit and hash-checked artwork export, not a self-contained rerun of all numerical results.

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
