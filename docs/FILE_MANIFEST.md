# Current CEP release file manifest

- `README.md`: publication mapping, scope, and reproduction level.
- `figures/Fig01`–`Fig06` `.svg/.png`: six current main figures.
- `figures/FigS07_Diagnostics.svg/.png`, `FigS08_PredictorEffects.svg/.png`: current supplementary figures.
- `figures/Fig01_CEP.drawio`: editable current workflow source.
- `figures/manifest_cep.json`: current figure and source-data SHA-256 manifest.
- `figures/Fig03_separation_source.json`, `figures/FigS07_source_manifest.json`, `figures/recorded_values.json`: locked figure provenance.
- `figures/archive/pre_cep/`: historical pre-CEP Fig.1 source, manifest, and reproduced Fig.7/Fig.8 assets; not current outputs.
- `scripts/reproduce_figures.py`: validates and exports current Fig01–Fig06, FigS07 and FigS08 locked artwork.
- `analysis/`: output-level diagnostic code, recorded tables and provenance. `analysis/Table05_source.csv` and `analysis/Table06_source.csv` are manuscript table sources.
- `results/figure_data/fig3_selected_cases.csv`: four locked Fig.3 identifiers and metrics, including panel (b) window 19.
- `results/figure_data/figS07_*.csv`: S07 aggregation, leave-one-log-out and configuration source data.
- `docs/FIGURES.md`: current figure/table mapping and reproduction boundary.
- `docs/FIGURE3_PROVENANCE.md`, `docs/FIGURES07_PROVENANCE.md`: case and S07 scientific provenance.
- `docs/PUBLICATION_V6_PROVENANCE.md`, `docs/PUBLICATION_V7_1_PROVENANCE.md`, `docs/FIG1_ICON_SOURCES.md`: historical pre-CEP publication records, not current figure instructions.
- `configs/`, `src/egosmooth/`, `scripts/` and `tests/`: frozen scientific definitions, code and checks.

The release does not add a signed manuscript, original nuScenes archives, original map files, complete prediction arrays, credentials, or private machine paths.
