# Historical publication v6 provenance — superseded

This record describes the historical v6 release only, not the current manuscript or reproduction output. The current anonymous-review release is documented in `docs/FIGURES.md` and the root `manifest_current.json`. The original v6 manifest and artwork are preserved in `figures/archive/pre_v7_1/`.

This release changes publication mapping and exports only. Current figures are Fig01–Fig07 and FigS07. Table 5 replaces the former timing-definition figure panel; Table 6 and Methods 2.6 replace former Fig08. No experiment, predictor output, scientific metric, or Supplement S1 identifier is changed.

Hashes are recorded in `figures/manifest_v6.json`. Artwork is imported from the locked v6 SVG/PNG source; the source PNGs were generated from the corresponding SVGs. The export script checks these hashes and produces byte-identical current assets, rather than claiming fresh raw-data reconstruction.

Table 5 retains full precision in `fig07_timestamp_sensitivity.csv`; Table 6 retains full precision in `fig08_kinematic_controls.csv`. Manuscript-precision CSVs are derived solely by selection, formatting and subtraction of the two saved percentages for Table 5's Difference column.

Fig.3(b) is the already locked case: scene `b0b26c1e5a1140e69598422f12ae1dc0`, sample `53a3b6ba49af484d9d0bab0ffb9dea01`, log `7a0fde44c3504eaeb18f9ad83bed65bc`, window `19`. The reference run and seed remain `P2B_042_log_primary_PositionalTransformer_s1` and 1. Publishing this record corrects an older snapshot; it does not select a new case.

S07 publication SVG/PNG are unchanged. Its three input CSVs and provenance accompany this release. Supplement S1 and S07 references remain intact.

For a review link, use the existing anonymous service with its identity filters; do not distribute an unfiltered checkout as an anonymous package. Local/public source metadata may identify authors, whereas the review mirror must be checked independently after refresh.
