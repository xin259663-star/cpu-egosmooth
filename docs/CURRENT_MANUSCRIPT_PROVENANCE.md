# Revised manuscript provenance and limits

The current manuscript has five main figures and five main tables. `manifest_current.json` is the local-byte SHA-256 source of truth for the five locked main SVGs, FigS07, retained historical FigS08 artwork, the current Table 5 source, and frozen scientific records. Historical filenames are not silently renamed: `results/tables/Table06_kinematic_controls.csv` supplies current Table 5, and `results/provenance/Fig03_case_selection.csv` supplies current Figure 2. The earlier six-figure manifest and SVGs remain available from Git commit `b062d14`; older journal-specific files remain under `figures/archive/`.

Current Figure 2(b) preserves the historical Fig. 3(b) selection: scene `b0b26c1e5a1140e69598422f12ae1dc0`, sample `53a3b6ba49af484d9d0bab0ffb9dea01`, log `7a0fde44c3504eaeb18f9ad83bed65bc`, window `19`. No case was reselected. The historical original-file hashes in Supplement S1.5 refer to the original package bytes, not to anonymous-mirror bytes. For local public-source paths and hashes use `manifest_current.json`; anonymous-mirror bytes require an independent public read-back because text and SVG metadata may be filtered.

## Public mirror hash read-back

On 2026-10-09, the original anonymous URL was read independently. The five current SVG paths and their public-byte SHA-256 values are recorded in each figure's `anonymous_mirror_sha256` field in `manifest_current.json`; the existing `sha256` fields remain the unfiltered source-byte hashes. The anonymous mirror rewrites RDF/metadata URLs in four SVGs, so those public-byte hashes differ from the source-byte hashes. Fig01 is byte-identical. FigS07/FigS08 SVG/PNG and the historical-filename source for current Table 5 were byte-identical. This distinction must be preserved in any provenance claim; a source-byte hash alone does not validate the filtered public SVG.

The three current `provenance/frozen_fig3_sources/` files are byte-identical between the local source and the audited anonymous ZIP. Their current public-byte hashes are in `figure_3_s1_source_trace[*].anonymous_sha256`. The previously recorded anonymous digests are retained separately as `historical_anonymous_sha256`; `original_sha256` refers to historical original-package bytes. Neither historical digest is a checksum for a current public path.

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

The complete historical primary split was recovered on 2026-10-10. `results/provenance/primary_split_log_tokens.json` and `.csv` disclose all 49 Train, 6 Validation-A, 6 Validation-B, and 7 Test log tokens. These are copied from the existing primary split, not inferred from counts or generated anew. The four groups are pairwise log-disjoint and contain 68 unique logs.

The original split SHA-256 is `6c4fbc453907b967850cb61e8a8e1d38197da64b7e4a33ac91f728e0484887fc`. It matches the split digest recorded in the historical formal dataset manifest. That manifest has SHA-256 `3d127e50b4ba61a06a72f5db04f376544ce1cd677928c23c5a648cf158a2a6eb`, matching all 50 primary predictor-seed run references. Split log/scene/window counts match the manuscript, and the seven Test tokens independently match all 2,901 records in the frozen Test index. Current exported identifier-file hashes are recorded in `manifest_current.json` under `split_identifier_sources`; original historical files and private paths are not redistributed.

This closes the split-identifier disclosure gap, but does not establish an end-to-end numerical rerun. Licensed data, predictions or checkpoints, and further implementation verification remain separate requirements.

## Verification scope

`scripts/reproduce_figures.py` checks frozen source and artwork hashes and exports the locked artwork. `scripts/reproduce_publication_tables.py` formats saved table source records. Neither command retrains a predictor or recomputes numerical results from raw nuScenes. Full numerical recomputation additionally requires licensed data, exact split identifiers, predictions or checkpoints, and validated implementation details not all present in this repository.
