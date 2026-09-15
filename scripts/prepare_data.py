
from __future__ import annotations
import argparse
from pathlib import Path
def main():
    p=argparse.ArgumentParser(); p.add_argument("--nuscenes-root", required=True, type=Path); p.add_argument("--output-dir", type=Path, default=Path("data/processed")); a=p.parse_args()
    if not a.nuscenes_root.exists(): raise SystemExit("nuScenes root not found. Obtain the dataset from the official provider; see docs/DATA.md.")
    raise SystemExit("The frozen preprocessing implementation requires author review before public full-pipeline release. Level-1 result reproduction is available now.")
if __name__ == "__main__": main()
