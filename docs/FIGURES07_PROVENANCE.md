# Supplementary Figure S07 Provenance

## Scope

Supplementary Figure S07 reports three descriptive sensitivity checks from frozen held-out Test outputs:

- panel (a): window-weighted and equal-log paired effects for ADE, FDE, and Shape;
- panel (b): the sign of the leave-one-log-out Shape effect for each of seven Test logs;
- panel (c): the direction and magnitude of the Shape effect under the Primary, IC1, and IC2 internal configurations.

Shape is the paper-facing name for the implementation metric `history_aware_mean_jerk`. It is a sampled-path geometric descriptor, not physical jerk.

## Source data

- `results/figure_data/figS07_aggregation_summary.csv` contains the exact aggregation results.
- `results/figure_data/figS07_lolo_effects.csv` contains all leave-one-log-out effects; panel (b) uses rows where `metric=history_aware_mean_jerk` for the Fixed-SG-minus-Raw and Selected-minus-Fixed contrasts.
- `results/figure_data/figS07_internal_configuration.csv` records the Primary, IC1, and IC2 Shape effects and frozen configuration definitions used in panel (c).

The locked publication files are `figures/FigS07_Diagnostics.png` and `figures/FigS07_Diagnostics.svg`. They were not regenerated during the provenance repair.

## Reproduction path

Run:

```powershell
python scripts/reproduce_figures.py --fig S07 --root .
```

This validates the saved source records and writes byte-identical locked SVG/PNG exports to `figures/reproduced/`. It does not recompute the experiments or regenerate a new S07 layout. The locked publication SVG and PNG remain the submission assets, with hashes in `figures/manifest_v6.json`.
