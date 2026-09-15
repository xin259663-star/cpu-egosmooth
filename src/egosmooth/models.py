from __future__ import annotations
import torch
from torch import nn

def flatten_input(x):
    return x.reshape(x.shape[0], -1)

class MLP(nn.Module):
    def __init__(self, hidden=64):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(20, hidden), nn.ReLU(), nn.Linear(hidden, hidden), nn.ReLU(), nn.Linear(hidden, 12))
    def forward(self, x):
        return self.net(flatten_input(x)).reshape(-1, 6, 2)

class _RNN(nn.Module):
    cell = nn.GRU
    def __init__(self, hidden=64):
        super().__init__()
        self.rnn = self.cell(5, hidden, batch_first=True)
        self.head = nn.Linear(hidden, 12)
    def forward(self, x):
        y, _ = self.rnn(x)
        return self.head(y[:, -1]).reshape(-1, 6, 2)

class GRU(_RNN):
    cell = nn.GRU

class LSTM(_RNN):
    cell = nn.LSTM

class TemporalCNN(nn.Module):
    def __init__(self, hidden=64):
        super().__init__()
        self.net = nn.Sequential(nn.Conv1d(5, hidden, 3, padding=1), nn.ReLU(), nn.Conv1d(hidden, hidden, 3, padding=1), nn.ReLU())
        self.head = nn.Linear(hidden, 12)
    def forward(self, x):
        return self.head(self.net(x.transpose(1, 2)).mean(-1)).reshape(-1, 6, 2)

class PositionalTransformer(nn.Module):
    def __init__(self, hidden=64):
        super().__init__()
        self.proj = nn.Linear(5, hidden)
        self.position = nn.Embedding(4, hidden)
        layer = nn.TransformerEncoderLayer(hidden, 4, 128, batch_first=True, dropout=0.0)
        self.encoder = nn.TransformerEncoder(layer, 2)
        self.head = nn.Linear(hidden, 12)
    def forward(self, x):
        pos = torch.arange(x.shape[1], device=x.device)
        y = self.encoder(self.proj(x) + self.position(pos)[None])
        return self.head(y.mean(1)).reshape(-1, 6, 2)

MODELS = {"MLP": MLP, "GRU": GRU, "LSTM": LSTM, "TemporalCNN": TemporalCNN, "PositionalTransformer": PositionalTransformer}
def build_model(name):
    return MODELS[name]()
def parameter_count(model):
    return sum(p.numel() for p in model.parameters() if p.requires_grad)
