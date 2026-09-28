# File manifest

- `README.md`, `CITATION.cff`, `LICENSE`: project overview, citation metadata and software license.
- `configs/`, `src/egosmooth/`: existing frozen scientific protocol and implementation, unchanged in the v6 release patch.
- `figures/Fig01.png/.svg` through `Fig07.png/.svg`: current main figures at 178 mm.
- `figures/FigS07_Diagnostics.png/.svg`: locked supplementary diagnostics.
- `figures/manifest_v6.json`: SHA-256 for current artwork and linked data, Table 5/6 mapping and superseded Fig08 status.
- `figures/archive/pre_v6/`: earlier PDF exports and Fig08 PNG; superseded artwork, not current outputs.
- `scripts/reproduce_figures.py`: checked export of Fig01–Fig07 + FigS07, with case/count validators.
- `scripts/reproduce_publication_tables.py`: Table 5/6 export from existing full-precision source CSVs.
- `results/tables/Table05_timing_sensitivity.csv`: manuscript-precision Table 5.
- `results/tables/Table06_kinematic_controls.csv`: manuscript-precision Table 6.
- `results/figure_data/fig07_timestamp_sensitivity.csv`: Table 5 full-precision source; historical filename retained.
- `results/figure_data/fig08_kinematic_controls.csv`: Table 6 full-precision source; historical filename retained.
- `results/figure_data/fig07_selection_sensitivity.csv`: current Fig.7 data.
- `results/figure_data/fig3_selected_cases.csv` and `results/provenance/Fig03*`: locked Fig.3/S1 case identity and metrics.
- `results/figure_data/figS07_*.csv`: S07 aggregation, LOLO and internal-configuration inputs.
- `docs/FIGURE3_PROVENANCE.md`, `docs/FIGURES07_PROVENANCE.md`, `docs/PUBLICATION_V6_PROVENANCE.md`: case, supplement and release records.
- `results/summary/formal_runs_summary.csv`: unchanged 50-run summary.
- `tests/`: scientific checks and current publication-export checks.

No author-manuscript DOCX/PDF, raw nuScenes archives, original map files, prediction NPZ, credentials or private machine paths are added by this patch. Source CSVs retain their existing scientific values.
