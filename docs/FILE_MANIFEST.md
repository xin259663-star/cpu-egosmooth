
# File Manifest

- `README.md`, `CITATION.cff`, and `LICENSE`: project overview, citation metadata, and BSD-3-Clause software license.
- `configs/`: frozen experiment, predictor, and post-processing configurations.
- `src/egosmooth/`: metrics, smoothing, selection, model, normalization, and alignment utilities.
- `scripts/`: scripts for reproducing tables and figures and for running the documented processing and evaluation steps.
- `tests/`: cardinality, alignment, metric, selection, leakage, citation, and reproducibility checks.
- `results/summary/formal_runs_summary.csv`: 50 formal model-seed runs with Raw, Fixed SG, Selected, and paired effects.
- `results/provenance/test_window_index.csv`: compact Test key/cardinality index.
- `results/figure_data/`: CSV inputs used by the plotting scripts.
- `results/provenance/fig3_selection_summary.json`: automatic Figure 3 selection provenance.
- `figures/Fig01`-`Fig08`: final manuscript-facing exports; `Fig03` is the four-case real-BEV qualitative figure.
- `figures/reproduced/`: outputs regenerated from public processed CSVs.

The Figure 3 script uses repository-relative CLI inputs and contains no local path. Editable artwork, raw nuScenes maps, complete metadata tables, and the selected-trajectory NPZ are excluded because they depend on separately obtained data or are not redistributed under the repository's data-sharing policy.
