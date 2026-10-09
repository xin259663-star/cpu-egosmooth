# File manifest

- `README.md`, `CITATION.cff`, `LICENSE`: project overview, citation metadata and software license.
- `configs/`, `src/egosmooth/`: existing frozen scientific protocol and implementation, unchanged in the v7.1 publication polish.
- `figures/Fig01_final.svg` through `figures/Fig05_final.svg`: current locked main figures.
- `figures/FigS07_Diagnostics.png/.svg`: current supplementary figure; `figures/FigS08_PredictorEffects.png/.svg` is retained historical artwork supporting revised Table S08.
- `manifest_current.json`: authoritative SHA-256 manifest for current artwork, scientific sources, and current Table 5 mapping.
- `figures/archive/pre_v6/`: earlier PDF exports and Fig08 PNG; superseded artwork, not current outputs.
- `scripts/reproduce_figures.py`: hash-checked export of Fig01-Fig05 + FigS07 and retained historical FigS08.
- `scripts/reproduce_publication_tables.py`: export from existing full-precision sources; current Table 5 is kinematic controls.
- `results/tables/Table05_timing_sensitivity.csv`: historical timing-sensitivity output, not current Table 5.
- `results/tables/Table06_kinematic_controls.csv`: current Table 5 source under historical filename.
- `results/figure_data/fig07_timestamp_sensitivity.csv`: historical timing-sensitivity source.
- `results/figure_data/fig08_kinematic_controls.csv`: current Table 5 full-precision source under historical filename.
- `results/figure_data/fig07_selection_sensitivity.csv`: current Fig.5(c) data under historical filename.
- `results/figure_data/fig3_selected_cases.csv` and `results/provenance/Fig03*`: locked current Fig.2/S1 case identity and metrics under historical filenames.
- `results/figure_data/figS07_*.csv`: S07 aggregation, LOLO and internal-configuration inputs.
- `docs/FIGURE3_PROVENANCE.md`, `docs/FIGURES07_PROVENANCE.md`, `docs/PUBLICATION_V7_1_PROVENANCE.md`: case, supplement and release records.
- `results/summary/formal_runs_summary.csv`: unchanged 50-run summary.
- `tests/`: scientific checks and current publication-export checks.

No author-manuscript DOCX/PDF, raw nuScenes archives, original map files, prediction NPZ, credentials or private machine paths are added by this patch. Source CSVs retain their existing scientific values.

- `figures/archive/pre_v7_1/`: superseded seven-figure v6 artwork and original manifest.
- `figures/Fig01_Protocol.drawio`: editable protocol diagram. SVG is the publication source for corresponding PNG.

Historical Fig1 icon-only patch v7.2 is retained for provenance; it is not the current publication mapping.

The superseded v7.3 artwork and manifest are retained under `figures/archive/superseded_v7_3/`. Current outputs are defined only by the root `manifest_current.json`.
