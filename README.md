# Pre-controller trajectory post-processing verification

This anonymous repository supports a pre-controller, output-level evaluation of short-horizon ego-trajectory post-processing on nuScenes. It does not demonstrate controller-in-the-loop performance, vehicle safety, comfort, or deployment feasibility.

## Current publication mapping

- Fig.1: pre-controller verification workflow
- Fig.2: data construction and role isolation
- Fig.3: qualitative held-out trajectory cases and pointwise separation insets
- Fig.4: paired effects and absolute means
- Fig.5: local degradation and interface consequences
- Fig.6: candidate composition and decision robustness
- Supplementary Fig.S07: aggregation, leave-one-log-out and configuration sensitivity
- Supplementary Fig.S08: predictor-stratified paired effects
- Table 5: timing-definition sensitivity (`analysis/Table05_source.csv`)
- Table 6: kinematic controls (`analysis/Table06_source.csv`)

The current figure files and SHA-256 hashes are listed in `figures/manifest_cep.json`. Older IET and pre-CEP figure files, if retained outside this overlay, are superseded and must not be described as current manuscript artwork.

## Reproduction level

`python scripts/reproduce_figures.py --fig all --root .` validates the locked source records and exports byte-identical publication SVG/PNG files to `figures/reproduced/`. This is a locked-artwork export. It does not retrain predictors, rebuild nuScenes map crops, or regenerate all panels from raw nuScenes data. `analysis/diagnostics.py` documents the post-hoc calculations on separately held frozen prediction arrays; those arrays and licensed nuScenes source files are not redistributed here.

Four Figure 3 case tokens and window indices are in `results/figure_data/fig3_selected_cases.csv`; the deterministic selection protocol is described in the supplementary material. Figure 3 inset source separations are in `figures/Fig03_separation_source.json`. S07 source CSVs and S08 recorded values are included. This CEP publication overlay adds no signed manuscript file or author metadata. The separately identifiable source repository has historical citation metadata; the anonymous review mirror must be checked independently for identity filtering after every refresh.
