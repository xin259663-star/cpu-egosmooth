# Reproducibility scope for the anonymous manuscript

## Current publication artwork

`python scripts/reproduce_figures.py --fig all --root .` verifies frozen scientific-source and locked-artwork hashes in the root `manifest_current.json`, then copies byte-identical Fig01-Fig05 SVGs, FigS07 SVG/PNG, and retained historical FigS08 SVG/PNG to the selected output directory. This is a checked publication-artwork export. It does **not** recompute panels from raw nuScenes data. Current Figure 2 map crops and the supplementary layouts are frozen artwork.

For current main SVGs the exporter accepts only the explicitly recorded source-byte SHA-256 or 4open-filtered public-byte SHA-256. It checks that the exported copy matches the exact input bytes. The three current Fig. 2 provenance records use their current anonymous-byte hashes; historical original-package hashes are identified separately in the manifest.

## Processed results and diagnostic definitions

`analysis/diagnostics.py` documents post-hoc output-level descriptor calculations on separately held frozen prediction arrays. Compact recorded sources for Table 5, Table 6, S07 and S08 are included. Original complete prediction arrays and licensed nuScenes assets are not redistributed. No controller-in-the-loop or closed-loop vehicle experiment is represented.

## Full pipeline

The `configs/`, `src/egosmooth/` and training/evaluation scripts retain scientific definitions and role isolation. A fresh raw-nuScenes-to-final-figure run requires separately licensed data, saved predictions or model retraining, and environment setup; it has not been validated here as a self-contained fresh-machine workflow. Test data are not used for training, checkpoint selection, or post-processing candidate selection.

Previous journal-specific Fig.7/Fig.8 files are archived under `figures/archive/superseded_journal_release/`, not emitted by the current figure command.
