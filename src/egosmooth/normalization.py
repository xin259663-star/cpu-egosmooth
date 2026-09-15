from __future__ import annotations
import json
from pathlib import Path
import numpy as np

class Normalizer:
    def __init__(self, mean, std):
        self.mean = np.asarray(mean, np.float64)
        self.std = np.asarray(std, np.float64)
    @classmethod
    def load(cls, path):
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        return cls(data["mean"], data["std"])
    def input(self, data):
        x = np.concatenate([data["history_xy"], data["history_v"][..., None], data["history_a"][..., None], data["history_yaw"][..., None]], -1)
        return ((x - self.mean) / self.std).astype(np.float32)
    def target(self, data):
        return ((data["future_xy"] - self.mean[:2]) / self.std[:2]).astype(np.float32)
    def inverse_target(self, target):
        return (np.asarray(target) * self.std[:2] + self.mean[:2]).astype(np.float32)
