
# CPU EgoSmooth

CPU EgoSmooth provides code and reproducibility materials for accuracy-constrained post-processing of short-horizon ego-trajectory predictions. The study separates displacement accuracy, sampled-path geometry, local paired effects, and selection sensitivity. It does not claim improved safety, comfort, physical jerk, closed-loop behavior, or complete autonomous-driving performance.

```bash
python scripts/reproduce_tables.py --results-root results
python scripts/reproduce_figures.py --fig all
```

## Paper

**Multidimensional Audit of Short-Horizon Open-Loop Ego-Trajectory Post-Processing under Accuracy-Constrained Selection**

Kexin Zhu ([ORCID](https://orcid.org/0009-0004-7456-9491)), Xu Xu ([ORCID](https://orcid.org/0000-0003-3602-1391))

Target journal: *IET Intelligent Transport Systems*

Article type: Original Research Paper

Repository: https://github.com/xin259663-star/cpu-egosmooth

## Repository structure

- `src/egosmooth/`: metrics, post-processing, model definitions, selection, and alignment checks
- `scripts/`: command-line entry points and figure/table reproduction
- `configs/`: experiment protocol, predictor, training, and candidate definitions
- `results/`: processed summaries, figure data, tables, and provenance
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

Figures 4-8 and the processed-result tables are regenerated from the included CSV files. Figure 3 requires the corresponding saved trajectory outputs and a local nuScenes installation; without them its script exits with an explanatory message.

## Figure 3 qualitative cases

Figure 3 contains four automatically selected real held-out Test windows:
(a) typical sampled-geometry change,
(b) near-preserved displacement accuracy with altered geometry,
(c) a positive-tail local-error case, and
(d) a Selected-versus-Fixed-SG trade-off.

The reference run is
`P2B_042_log_primary_PositionalTransformer_s1`
(Pos-Transformer, seed 1); the selected smoother is QReg-L1
(implementation ID `qreg_l1`); `manual_override=false`.

Map context is used only for visualization and is not provided to predictors,
post-processing, candidate selection, or quantitative evaluation.

See `docs/FIGURE3_PROVENANCE.md`.

## Reproducibility levels

- **Level 1, processed results to figures/tables:** Verified.
- **Level 2, saved predictions to metrics/results:** Verified using the original saved predictions. These prediction files are not included in this repository.
- **Level 3, raw nuScenes through held-out evaluation:** Partially documented. This level requires the original nuScenes data and additional environment setup. The scientific protocol and configurations are documented, but the full raw-data-to-evaluation pipeline has not been validated as a self-contained fresh-machine workflow.

The processed-result reproduction path is CPU-friendly; the original predictor training used CUDA.

## Citation

See `CITATION.cff`. The public repository is https://github.com/xin259663-star/cpu-egosmooth. DOI metadata are omitted until they exist.

## License

The repository software is released under the BSD 3-Clause License; see `LICENSE`. nuScenes and all third-party datasets or assets are not covered by this software license.

## Acknowledgements and third-party data

The experiments use nuScenes. Dataset access and use remain governed by the provider's applicable terms. No affiliation with or endorsement by the dataset provider is implied.
