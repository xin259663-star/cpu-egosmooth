
# Experiment Protocol

The primary experiment contains 50 formal runs: five predictors (MLP, GRU, LSTM, TemporalCNN, and PositionalTransformer) across seeds 0-9. H=4, T=6, and nominal dt=0.5 s.

| Role | Logs | Scenes | Windows | Purpose |
| --- | ---: | ---: | ---: | --- |
| Training | 49 | 597 | 18,623 | Parameter estimation and normalization |
| Validation-A | 6 | 80 | 2,489 | Checkpoint selection |
| Validation-B | 6 | 80 | 2,486 | Post-processing candidate selection |
| Held-out Test | 7 | 93 | 2,901 | Final evaluation only |

Test is never used for training, checkpoint selection, post-processing candidate selection, or hyperparameter selection.

Fixed SG is Savitzky-Golay `(window=5, polyorder=2)`, implementation ID `sg_w5_p2`. For the primary zero-tolerance selection, feasible Validation-B candidates first satisfy `delta_ADE <= 0` and `delta_FDE <= 0`. The feasible set is then ranked lexicographically by Shape, ADE, FDE, and frozen enumeration order. The conditions are sequential, not a merged score.
