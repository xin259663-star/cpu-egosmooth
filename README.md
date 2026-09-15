
# CPU EgoSmooth

CPU EgoSmooth provides code and reproducibility materials for accuracy-constrained post-processing of short-horizon ego-trajectory predictions. The study separates displacement accuracy, sampled-path geometry, local paired costs, and candidate-selection stability. It does not claim improved safety, comfort, physical jerk, closed-loop behavior, or complete autonomous-driving performance.

```bash
python scripts/reproduce_tables.py --results-root results
python scripts/reproduce_figures.py --fig all
```

## Paper

**Accuracy-Constrained Evaluation of Geometric Effects in Short-Horizon Open-Loop Ego-Trajectory Post-Processing**

Kexin Zhu ([ORCID](https://orcid.org/0009-0004-7456-9491)), Xu Xu ([ORCID](https://orcid.org/0000-0003-3602-1391))

Target journal: *IET Intelligent Transport Systems*

Article type: Original Research Paper

## Repository structure

- `src/egosmooth/`: metrics, post-processing, model definitions, selection, and alignment checks
- `scripts/`: public command-line entry points and figure/table reproduction
- `configs/`: frozen protocol, predictor, training, and candidate definitions
- `results/`: compact processed summaries, figure data, tables, and provenance
- `figures/`: final manuscript figures and regenerated processed-result figures
- `docs/`: data, protocol, figure, and reproducibility documentation

## Quick start

```bash
python -m venv .venv
# Windows
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python -m pip install -e .
# Linux/macOS
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pip install -e .
```

## Data

The study uses the publicly available nuScenes trainval release, which must be obtained separately from the official provider under its applicable terms. This repository does not redistribute original sensor data, maps, complete annotation tables, or dataset archives. Predictors use ego-state-derived inputs; map context is used only for the Figure 3 visualization. See `docs/DATA.md`.

## Reproduce tables and figures

```bash
python scripts/reproduce_tables.py --results-root results
python scripts/reproduce_figures.py --fig all
pytest -q
```

Figures 4-8 and the processed-result tables are regenerated from public CSV files. Figure 3 requires locally available reviewed trajectory outputs and nuScenes map data; without them its script exits with an explanatory message.

## Figure 3 qualitative cases

The formal Figure 3 contains four automatically selected real held-out Test windows: (a) typical geometry reduction, (b) accuracy preserved with altered geometry, (c) local error increase, and (d) Selected differs from Fixed SG. The reference run is `P2B_042_log_primary_PositionalTransformer_s1` (Pos-Transformer, seed 1); the selected smoother is QReg-L1 (implementation ID `qreg_l1`); `manual_override=false`. Map context is visualization only and is not provided to predictors, post-processing, candidate selection, or quantitative evaluation. See `docs/FIGURE3_PROVENANCE.md`.

## Reproducibility levels

- **Level 1, processed results to figures/tables: VERIFIED.**
- **Level 2, saved predictions to metrics/results: VERIFIED INTERNALLY; complete predictions are not redistributed in this compact repository.**
- **Level 3, raw nuScenes through held-out evaluation: PARTIALLY DOCUMENTED / REVIEW GATE.**

Archived formal training used CUDA, while the Level-1 reproduction path is CPU-friendly. The repository does not claim that every original training step was CPU-only.

## Citation

See `CITATION.cff`. Repository URL and DOI metadata are omitted until they exist.

## License

The repository software is released under the BSD 3-Clause License; see `LICENSE`. nuScenes and all third-party datasets or assets are not covered by this software license.

## Acknowledgements and third-party data

The experiments use nuScenes. Dataset access and use remain governed by the provider's applicable terms. No affiliation with or endorsement by the dataset provider is implied.
