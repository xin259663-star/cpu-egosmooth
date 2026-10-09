# Revised manuscript provenance and limits

The current manuscript has five main figures and five main tables. `manifest_current.json` is the local-byte SHA-256 source of truth for the five locked main SVGs, FigS07, retained historical FigS08 artwork, the current Table 5 source, and frozen scientific records. Historical filenames are not silently renamed: `results/tables/Table06_kinematic_controls.csv` supplies current Table 5, and `results/provenance/Fig03_case_selection.csv` supplies current Figure 2. The earlier six-figure manifest and SVGs remain available from Git commit `b062d14`; older journal-specific files remain under `figures/archive/`.

Current Figure 2(b) preserves the historical Fig. 3(b) selection: scene `b0b26c1e5a1140e69598422f12ae1dc0`, sample `53a3b6ba49af484d9d0bab0ffb9dea01`, log `7a0fde44c3504eaeb18f9ad83bed65bc`, window `19`. No case was reselected. The historical original-file hashes in Supplement S1.5 refer to the original package bytes, not to anonymous-mirror bytes. For local public-source paths and hashes use `manifest_current.json`; anonymous-mirror bytes require an independent public read-back because text and SVG metadata may be filtered.

## Log identifier availability

`results/provenance/test_window_index.csv` contains 2,901 held-out Test windows and the following seven distinct Test log tokens:

| Test log token | Windows |
| --- | ---: |
| `4de1fda752ae4cf8b650a5245734eb4c` | 1063 |
| `69271ec7af1f446ca16820ac46d2047a` | 632 |
| `7a0fde44c3504eaeb18f9ad83bed65bc` | 460 |
| `d7fd2bb9696d43af901326664e42340b` | 124 |
| `eda311bda86f4e54857b0554639d6426` | 187 |
| `f61e86a4241b484484da143725dce8fc` | 280 |
| `f93e8d66ce4b4fbea7062d19b1fe29fb` | 155 |

The current public records state 49/6/6 Train/Validation-A/Validation-B log counts, but do not contain their token lists. Their exact identifiers remain unverified. Counts and the seven Test tokens cannot reconstruct those lists. Do not claim that this repository alone supports an end-to-end numerical rerun.

## Verification scope

`scripts/reproduce_figures.py` checks frozen source and artwork hashes and exports the locked artwork. `scripts/reproduce_publication_tables.py` formats saved table source records. Neither command retrains a predictor or recomputes numerical results from raw nuScenes. Full numerical recomputation additionally requires licensed data, exact split identifiers, predictions or checkpoints, and validated implementation details not all present in this repository.
