# Current anonymous-review publication figures

The revised manuscript has five main figures, `Fig01`-`Fig05`, supplied as locked SVG artwork. `FigS07_Diagnostics` remains a supplementary figure; `FigS08_PredictorEffects` is retained as historical artwork supporting the revised Supplementary Table S08, not a current supplementary figure caption. The source-of-truth mapping and SHA-256 hashes are in the root `manifest_current.json`.

Earlier journal-specific diagrams, manifests, and reproduced Fig.7/Fig.8 outputs are retained under `archive/superseded_journal_release/`. They are historical and are not current publication artwork.

Run `python scripts/reproduce_figures.py --fig all --root .` from the repository root to verify saved source records and export byte-identical SVG/PNG files to `figures/reproduced/`. This is a locked-artwork export, not a reconstruction of every panel from raw nuScenes data.
