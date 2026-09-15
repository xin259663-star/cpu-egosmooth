
from __future__ import annotations
import argparse
from pathlib import Path
def main():
    p=argparse.ArgumentParser(); p.add_argument("--config", type=Path, default=Path("configs/experiment/protocol.yaml")); p.parse_args()
    raise SystemExit("The frozen full-pipeline wrapper for generate Raw predictions is documented but remains review-required; no Test data are used for development decisions.")
if __name__ == "__main__": main()
