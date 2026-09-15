
# Data

The nuScenes dataset is not redistributed. Obtain the trainval release from the official nuScenes channel and place it outside version control. The expected root contains `v1.0-trainval/`, `samples/`, `sweeps/`, and `maps/` as required by the chosen reproduction level. Predictors use ego-state-derived tensors only. Map content is needed solely to recreate the optional real-BEV qualitative background.

`example/` is intentionally empty in this review candidate because no synthetic payload is represented as a paper result. `processed/` contains no raw dataset records.
