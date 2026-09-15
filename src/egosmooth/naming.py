
DISPLAY_NAMES = {
    "raw": "Raw",
    "sg_w5_p2": "Fixed SG(5,2)",
    "qreg_l1": "QReg-L1",
    "qreg_l01": "QReg-L0.1",
    "PositionalTransformer": "Pos-Transformer",
    "TemporalCNN": "TemporalCNN",
}

def display_name(identifier: str) -> str:
    return DISPLAY_NAMES.get(identifier, identifier)
