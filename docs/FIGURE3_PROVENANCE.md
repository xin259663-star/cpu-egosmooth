
# Figure 3 Provenance

## Formal identity

- Figure role: representative qualitative effects on real held-out Test ego trajectories
- Reference run: `P2B_042_log_primary_PositionalTransformer_s1`
- Model: PositionalTransformer (paper-facing: Pos-Transformer)
- Seed: 1
- Selected smoother: QReg-L1
- Implementation ID: `qreg_l1`
- Manual override: `false`
- Formal public key: `run_id + scene_token + sample_token`

## Reference-run selection

The reference run was selected automatically from eligible formal runs whose selected candidate was QReg-L1 or QReg-L0.1. Six run-level paired-effect components were robust-scaled by median and interquartile range. The eligible run nearest the six-dimensional median effect vector was selected, with deterministic ordering. The complete selected-run record is stored in `results/provenance/fig3_selection_summary.json`.

## Four deterministic cases

| Panel | Role | Scene token | Sample token | Window | Selection rule |
| --- | --- | --- | --- | ---: | --- |
| (a) | Typical geometry reduction | `36e3167610cc48eabcaad06a72479ac7` | `e7eb475f0434413fa8f207a2fc113a06` | 9 | Negative Fixed-minus-Raw Shape change closest to the negative-change median, with accuracy-change tie-break |
| (b) | Accuracy preserved, geometry altered | `64a3a2d22172406c848f2a92275808ba` | `1f60f2715ba14d4c85a64f2aca576862` | 3 | Small absolute ADE/FDE change, then most negative non-outer-fence Shape change |
| (c) | Local error increase | `634e7fbfe29c4a72b1ceb692b1d2ab44` | `6c91a4e361c94bd7b976f7a971cd03d3` | 12 | Positive-tail Fixed-minus-Raw error severity nearest one, preferring negative Shape change |
| (d) | Selected differs from Fixed SG | `696a45dbd11346b794fdce43fa0a1770` | `0d45f0bedc6d455ea5a28cb4939c910d` | 13 | Selected-minus-Fixed sign pattern (-,+,-), then robust distance to the all-window median effect vector |

## Case metrics

| Panel | Raw ADE | Fixed SG ADE | QReg-L1 ADE | Raw FDE | Fixed SG FDE | QReg-L1 FDE | Raw Shape | Fixed SG Shape | QReg-L1 Shape |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| (a) | 0.334987 | 0.329416 | 0.326012 | 0.797630 | 0.810424 | 0.797630 | 0.644348 | 0.320664 | 0.265214 |
| (b) | 0.551906 | 0.551659 | 0.549259 | 1.483071 | 1.485804 | 1.483071 | 1.211305 | 0.344179 | 0.344683 |
| (c) | 0.317455 | 0.325753 | 0.323080 | 0.730106 | 0.747476 | 0.730106 | 1.040881 | 0.226565 | 0.393409 |
| (d) | 0.468194 | 0.468415 | 0.468161 | 0.564947 | 0.557741 | 0.564947 | 1.333180 | 1.229188 | 1.159827 |

The authoritative identifiers and Raw/Fixed/Selected ADE, FDE, and Shape values are in `results/figure_data/fig3_selected_cases.csv`. In case of any transcription discrepancy, that CSV and `fig3_selection_summary.json` govern.

## Map source and model boundary

The BEV background is rendered from the official nuScenes semantic-prior map using scene, sample, log, sample-data, ego-pose, and map-location provenance to recover the anchor pose. It is visualization only. Map content is not a predictor input and is not used by post-processing, candidate selection, or quantitative evaluation. The repository contains the rendered manuscript figure but not the original map assets, map crops, annotation tables, or trajectory NPZ.
