# Current publication figures

The current manuscript uses Fig.1–Fig.7 and Fig.S07. Table 5 contains timing-definition sensitivity; Table 6 contains kinematic controls. Shape equations remain in Methods 2.6.

| Display | Role |
|---|---|
| Fig.1 | Workflow |
| Fig.2 | Data protocol |
| Fig.3 | Qualitative cases |
| Fig.4 | Paired effects / absolute means |
| Fig.5 | Local error / boundary |
| Fig.6 | Predictor dependence / composition |
| Fig.7 | Selection-rule sensitivity |
| Table 5 | Timing-definition sensitivity |
| Table 6 | Kinematic controls |
| Fig.S07 | Supplementary diagnostics |

Current locked files are `figures/Fig01.png/.svg` through `Fig07.png/.svg` and `FigS07_Diagnostics.png/.svg`. `figures/manifest_v6.json` records SHA-256, source-data references and superseded mappings.

```bash
python scripts/reproduce_figures.py --fig all --root .
python scripts/reproduce_publication_tables.py --root .
```

The first command checks saved selection counts and locked case identifiers, then exports the reviewed artwork byte-for-byte to `figures/reproduced/`. It does not retrain predictors, regenerate trajectories or recompute map crops. The second exports Table 5/6 from unchanged processed CSVs at manuscript precision; full precision remains in the source CSVs.

Fig.7 uses `results/figure_data/fig07_selection_sensitivity.csv`, with three predefined settings and straight visual guides, not a fitted continuous response. The older filename `fig07_timestamp_sensitivity.csv` is retained as Table 5 source only. Likewise, `fig08_kinematic_controls.csv` is Table 6 source only, not an instruction to generate Fig.8.

Former Fig.8 is superseded by Table 6 + Methods 2.6 equations. Older PNG/PDF artwork is archival, not a current reproduction output. See `figures/archive/pre_v6/README.md`.

Fig.3 uses the unchanged locked reference run and four cases in `docs/FIGURE3_PROVENANCE.md`. S1 identifiers and deterministic selection rules are not changed. Fig.S07 remains locked; see `docs/FIGURES07_PROVENANCE.md`.

Official nuScenes semantic-prior map context is visualization-only. Underlying nuScenes datasets, original maps and prediction NPZ files are not redistributed. Frozen map-context artwork remains subject to the dataset provider's terms.
