# CEP manuscript figure and table mapping

| Manuscript item | Current role | Publication asset or source |
|---|---|---|
| Fig.1 | Pre-controller verification workflow | `figures/Fig01.svg`, `Fig01.png`, `Fig01_CEP.drawio` |
| Fig.2 | Data construction and role isolation | `figures/Fig02.svg`, `Fig02.png` |
| Fig.3 | Qualitative held-out cases and separation insets | `figures/Fig03.svg`, `Fig03.png` |
| Fig.4 | Paired effects and absolute means | `figures/Fig04.svg`, `Fig04.png` |
| Fig.5 | Local degradation and interface consequences | `figures/Fig05.svg`, `Fig05.png` |
| Fig.6 | Candidate composition and decision robustness | `figures/Fig06.svg`, `Fig06.png` |
| Fig.S07 | Aggregation, leave-one-log-out and configuration diagnostics | `figures/FigS07_Diagnostics.svg`, `.png` |
| Fig.S08 | Predictor-stratified paired effects | `figures/FigS08_PredictorEffects.svg`, `.png` |
| Table 5 | Timing-definition sensitivity | `analysis/Table05_source.csv` |
| Table 6 | Kinematic controls | `analysis/Table06_source.csv` |

`figures/manifest_cep.json` records current asset hashes. Figure 3 locked identifiers are in `results/figure_data/fig3_selected_cases.csv`; panel (b) has window 19. Its deterministic selection rules are documented in `docs/FIGURE3_PROVENANCE.md` and Supplement S1. Saved Figure 3 inset separation values are in `figures/Fig03_separation_source.json`.

Run `python scripts/reproduce_figures.py --fig all --root .` for a verified, byte-identical export of current SVG/PNG artwork. The script does not retrain models, regenerate trajectories, recompute map crops, or claim raw-data-to-figure reproduction. S07 has three accompanying source CSVs; S08 recorded values are in `figures/recorded_values.json`.

Previous IET figure mappings and numbered Fig.7/Fig.8 artwork are superseded. Their historical files remain under `figures/archive/` and are not current reproduction outputs. Scientific source CSVs with historical `fig07`/`fig08` filenames remain in `results/figure_data/` for provenance, but those filenames are not instructions to create current Fig.7 or Fig.8.

Official nuScenes semantic-prior maps are visualization context only. Original dataset/map assets and complete saved prediction arrays are not redistributed here.
