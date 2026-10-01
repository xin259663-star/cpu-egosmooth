# Reproducibility scope for the CEP release

## Current publication artwork

`python scripts/reproduce_figures.py --fig all --root .` verifies source-record and locked-artwork hashes in `figures/manifest_cep.json`, then copies byte-identical Fig01–Fig06 and FigS07–FigS08 SVG/PNG files to `figures/reproduced/`. This is a checked publication-artwork export. It does **not** recompute all panels from raw nuScenes data. Figure 3 map crops and S07 layout are frozen artwork.

## Processed results and diagnostic definitions

`analysis/diagnostics.py` documents post-hoc output-level descriptor calculations on separately held frozen prediction arrays. Compact recorded sources for Table 5, Table 6, S07 and S08 are included. Original complete prediction arrays and licensed nuScenes assets are not redistributed. No controller-in-the-loop or closed-loop vehicle experiment is represented.

## Full pipeline

The `configs/`, `src/egosmooth/` and training/evaluation scripts retain scientific definitions and role isolation. A fresh raw-nuScenes-to-final-figure run requires separately licensed data, saved predictions or model retraining, and environment setup; it has not been validated here as a self-contained fresh-machine workflow. Test data are not used for training, checkpoint selection, or post-processing candidate selection.

Previous IET-era reproduced Fig.7/Fig.8 files are archived in `figures/archive/pre_cep/reproduced/`, not emitted by the current figure command.
