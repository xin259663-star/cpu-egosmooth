# Current anonymous-review publication figures

The current manuscript has six main figures, `Fig01`-`Fig06`, supplied as locked SVG artwork. The supplement has `FigS07_Diagnostics` and `FigS08_PredictorEffects`, supplied as SVG and PNG. The source-of-truth mapping and SHA-256 hashes are in the root `manifest_current.json`.

Earlier journal-specific diagrams, manifests, and reproduced Fig.7/Fig.8 outputs are retained under `archive/superseded_journal_release/`. They are historical and are not current publication artwork.

Run `python scripts/reproduce_figures.py --fig all --root .` from the repository root to verify saved source records and export byte-identical SVG/PNG files to `figures/reproduced/`. This is a locked-artwork export, not a reconstruction of every panel from raw nuScenes data.
