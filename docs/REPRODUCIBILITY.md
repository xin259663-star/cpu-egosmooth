# Reproducibility scope for the anonymous manuscript

## Current publication artwork

`python scripts/reproduce_figures.py --fig all --root .` verifies frozen scientific-source and locked-artwork hashes in the root `manifest_current.json`, then copies byte-identical Fig01-Fig06 SVGs and FigS07-FigS08 SVG/PNG files to the selected output directory. This is a checked publication-artwork export. It does **not** recompute panels from raw nuScenes data. Figure 3 map crops and S07/S08 layouts are frozen artwork.

## Processed results and diagnostic definitions

`analysis/diagnostics.py` documents post-hoc output-level descriptor calculations on separately held frozen prediction arrays. Compact recorded sources for Table 5, Table 6, S07 and S08 are included. Original complete prediction arrays and licensed nuScenes assets are not redistributed. No controller-in-the-loop or closed-loop vehicle experiment is represented.

## Full pipeline

The `configs/`, `src/egosmooth/` and training/evaluation scripts retain scientific definitions and role isolation. A fresh raw-nuScenes-to-final-figure run requires separately licensed data, saved predictions or model retraining, and environment setup; it has not been validated here as a self-contained fresh-machine workflow. Test data are not used for training, checkpoint selection, or post-processing candidate selection.

Previous journal-specific Fig.7/Fig.8 files are archived under `figures/archive/superseded_journal_release/`, not emitted by the current figure command.
