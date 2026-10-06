# Current publication figures

The current manuscript uses Fig.1–Fig.6 and Fig.S07. Table 5 contains timing-definition sensitivity; Table 6 contains kinematic controls. Shape equations remain in Methods 2.6.

| Display | Role |
|---|---|
| Fig.1 | Study protocol and analysis map |
| Fig.2 | Data protocol |
| Fig.3 | Qualitative cases |
| Fig.4 | Paired effects / absolute means |
| Fig.5 | Local frequency / tail / boundary consequences |
| Fig.6 | Predictor dependence / composition / selection-rule sensitivity |
| Table 5 | Timing-definition sensitivity |
| Table 6 | Kinematic controls |
| Fig.S07 | Supplementary diagnostics |

Current locked files are `figures/Fig01_final.svg` through `figures/Fig06_final.svg`, plus `figures/FigS07_Diagnostics.png/.svg` and `figures/FigS08_PredictorEffects.png/.svg`. The root `manifest_current.json` records their SHA-256 hashes, frozen scientific-source hashes, Table 5/6 sources, and the fixed Fig. 3 provenance. Earlier publication artwork and manifests are superseded archives only.

```bash
python scripts/reproduce_figures.py --fig all --root .
python scripts/reproduce_publication_tables.py --root .
```

The first command checks saved selection counts and locked case identifiers, then exports the reviewed artwork byte-for-byte to `figures/reproduced/`. It does not retrain predictors, regenerate trajectories or recompute map crops. The second exports Table 5/6 from unchanged processed CSVs at manuscript precision; full precision remains in the source CSVs.

Fig.6(c) uses `results/figure_data/fig07_selection_sensitivity.csv`, with three predefined settings and straight visual guides, not a fitted continuous response. The older filename `fig07_timestamp_sensitivity.csv` is retained as Table 5 source only. Likewise, `fig08_kinematic_controls.csv` is Table 6 source only, not an instruction to generate Fig.8.

Former Fig.8 is superseded by Table 6 + Methods 2.6 equations. Older PNG/PDF artwork is archival, not a current reproduction output. See `figures/archive/pre_v6/README.md`.

Fig.3 uses the unchanged locked reference run and four cases in `docs/FIGURE3_PROVENANCE.md`. S1 identifiers and deterministic selection rules are not changed. Fig.S07 remains locked; see `docs/FIGURES07_PROVENANCE.md`.

Official nuScenes semantic-prior map context is visualization-only. Underlying nuScenes datasets, original maps and prediction NPZ files are not redistributed. Frozen map-context artwork remains subject to the dataset provider's terms.

Former v6 Fig.7 is merged into Fig.6(c), not deleted as scientific evidence. Historical v6 artwork is in figures/archive/pre_v7_1/. The Fig.6(a) matrix uses signed, column-specific intensity; colours do not independently identify strategies. Numeric units differ by column.

Historical Fig1 icon-only patch v7.2: five original Tabler Outline SVGs replaced the prior schematic symbols. Its provenance and MIT notice remain under `docs/FIG1_ICON_SOURCES.md` and `figures/icon_sources/tabler/`.

Historical Fig1 patch v7.3 and its manifest are retained under `figures/archive/superseded_v7_3/`; they are not current outputs.
