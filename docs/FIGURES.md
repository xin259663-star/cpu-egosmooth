# Current publication figures

The revised manuscript uses Fig.1-Fig.5 and Fig.S07. Current Table 5 contains kinematic controls. Historical timing-definition sensitivity is retained as supporting material, not current Table 5. Shape equations remain in Methods 2.6.

| Display | Role |
|---|---|
| Fig.1 | Study protocol and analysis map |
| Fig.2 | Qualitative cases (historical Fig.3) |
| Fig.3 | Paired effects / absolute means (historical Fig.4) |
| Fig.4 | Local frequency / tail / boundary consequences (historical Fig.5) |
| Fig.5 | Predictor dependence / composition / selection-rule sensitivity (historical Fig.6) |
| Table 5 | Kinematic controls (historical Table 6) |
| Fig.S07 | Supplementary diagnostics |
| Table S08 | Predictor-stratified paired effects; historical FigS08 artwork retained |

Current locked main figures are `figures/Fig01_final.svg` through `figures/Fig05_final.svg`; `figures/FigS07_Diagnostics.png/.svg` is supplementary. Historical `figures/FigS08_PredictorEffects.png/.svg` remains available as source artwork. The root `manifest_current.json` records exact hashes, frozen scientific-source hashes, the current Table 5 source under its historical filename, and unchanged case provenance. Earlier publication artwork and manifests are superseded archives only.

```bash
python scripts/reproduce_figures.py --fig all --root .
python scripts/reproduce_publication_tables.py --root .
```

The first command checks locked hashes and exports reviewed artwork byte-for-byte. It does not retrain predictors, regenerate trajectories or recompute map crops. The second exports the current Table 5 kinematic controls and historical timing sensitivity from unchanged processed CSVs at manuscript precision; full precision remains in the source CSVs.

Current Fig.5(c) uses `results/figure_data/fig07_selection_sensitivity.csv`, with three predefined settings and straight visual guides, not a fitted continuous response. The historical filename `fig07_timestamp_sensitivity.csv` remains a timing-sensitivity source; `fig08_kinematic_controls.csv` is the current Table 5 source, not an instruction to generate Fig.8.

Former Fig.8 is superseded by current Table 5 + Methods 2.6 equations. Older PNG/PDF artwork is archival, not a current reproduction output. See `figures/archive/pre_v6/README.md`.

Current Fig.2 uses the unchanged locked reference run and four historical Fig.3 cases in `docs/FIGURE3_PROVENANCE.md`. S1 identifiers and deterministic selection rules are not changed. Fig.S07 remains locked; see `docs/FIGURES07_PROVENANCE.md`.

Official nuScenes semantic-prior map context is visualization-only. Underlying nuScenes datasets, original maps and prediction NPZ files are not redistributed. Frozen map-context artwork remains subject to the dataset provider's terms.

Former v6 Fig.7 is merged into current Fig.5(c), not deleted as scientific evidence. Historical v6 artwork is in `figures/archive/pre_v7_1/`. The current Fig.5(a) matrix uses signed, column-specific intensity; colours do not independently identify strategies. Numeric units differ by column.

Historical Fig1 icon-only patch v7.2: five original Tabler Outline SVGs replaced the prior schematic symbols. Its provenance and MIT notice remain under `docs/FIG1_ICON_SOURCES.md` and `figures/icon_sources/tabler/`.

Historical Fig1 patch v7.3 and its manifest are retained under `figures/archive/superseded_v7_3/`; they are not current outputs.
