# File manifest

- `README.md`, `CITATION.cff`, `LICENSE`: project overview, citation metadata and software license.
- `configs/`, `src/egosmooth/`: existing frozen scientific protocol and implementation, unchanged in the v7.1 publication polish.
- `figures/Fig01.png/.svg` through `Fig06.png/.svg`: current main figures at 178 mm.
- `figures/Fig01_final.svg` through `figures/Fig06_final.svg`: current locked main figures.
- `figures/FigS07_Diagnostics.png/.svg` and `figures/FigS08_PredictorEffects.png/.svg`: current locked supplementary figures.
- `manifest_current.json`: authoritative SHA-256 manifest for current artwork, scientific sources, and Table 5/6.
- `figures/archive/pre_v6/`: earlier PDF exports and Fig08 PNG; superseded artwork, not current outputs.
- `scripts/reproduce_figures.py`: hash-checked export of Fig01–Fig06 + FigS07/S08.
- `scripts/reproduce_publication_tables.py`: Table 5/6 export from existing full-precision source CSVs.
- `results/tables/Table05_timing_sensitivity.csv`: manuscript-precision Table 5.
- `results/tables/Table06_kinematic_controls.csv`: manuscript-precision Table 6.
- `results/figure_data/fig07_timestamp_sensitivity.csv`: Table 5 full-precision source; historical filename retained.
- `results/figure_data/fig08_kinematic_controls.csv`: Table 6 full-precision source; historical filename retained.
- `results/figure_data/fig07_selection_sensitivity.csv`: current Fig.6(c) data.
- `results/figure_data/fig3_selected_cases.csv` and `results/provenance/Fig03*`: locked Fig.3/S1 case identity and metrics.
- `results/figure_data/figS07_*.csv`: S07 aggregation, LOLO and internal-configuration inputs.
- `docs/FIGURE3_PROVENANCE.md`, `docs/FIGURES07_PROVENANCE.md`, `docs/PUBLICATION_V7_1_PROVENANCE.md`: case, supplement and release records.
- `results/summary/formal_runs_summary.csv`: unchanged 50-run summary.
- `tests/`: scientific checks and current publication-export checks.

No author-manuscript DOCX/PDF, raw nuScenes archives, original map files, prediction NPZ, credentials or private machine paths are added by this patch. Source CSVs retain their existing scientific values.

- `figures/archive/pre_v7_1/`: superseded seven-figure v6 artwork and original manifest.
- `figures/Fig01_Protocol.drawio`: editable protocol diagram. SVG is the publication source for corresponding PNG.

Historical Fig1 icon-only patch v7.2 is retained for provenance; it is not the current publication mapping.

The superseded v7.3 artwork and manifest are retained under `figures/archive/superseded_v7_3/`. Current outputs are defined only by the root `manifest_current.json`.
