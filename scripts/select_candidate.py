
from __future__ import annotations
import argparse
from pathlib import Path
import pandas as pd
from egosmooth.selection import select_validation_b_candidate

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--validation-b-csv", required=True, type=Path)
    args = parser.parse_args()
    print(select_validation_b_candidate(pd.read_csv(args.validation_b_csv)).to_json())

if __name__ == "__main__":
    main()
