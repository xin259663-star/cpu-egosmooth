# Current CEP publication figures

The current manuscript has six main figures, `Fig01`–`Fig06`. The supplement has `FigS07_Diagnostics` and `FigS08_PredictorEffects`. Each current figure is supplied as SVG and PNG. The source-of-truth mapping and SHA-256 hashes are in `manifest_cep.json`.

`Fig01_CEP.drawio` is the editable source for the current workflow. The files in `archive/pre_cep/`, including the old Fig.1 diagram, old manifest, and previously reproduced Fig.7/Fig.8 outputs, are historical and are not current CEP publication artwork.

Run `python scripts/reproduce_figures.py --fig all --root .` from the repository root to verify saved source records and export byte-identical SVG/PNG files to `figures/reproduced/`. This is a locked-artwork export, not a reconstruction of every panel from raw nuScenes data.
