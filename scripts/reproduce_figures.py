"""Validate frozen sources and export the current locked publication figures."""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path

CURRENT = tuple(f"Fig{i:02d}" for i in range(1, 7)) + ("FigS07", "FigS08")

def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--fig", default="all")
    parser.add_argument("--output", type=Path, default=Path("reproduced_figures"))
    args = parser.parse_args()
    root = args.root.resolve()
    manifest = json.loads((root / "manifest_current.json").read_text(encoding="utf-8"))
    keys = CURRENT if args.fig.lower() == "all" else (args.fig,)
    if not all(k in CURRENT for k in keys):
        parser.error("Current set: Fig01–Fig06, FigS07, FigS08")
    for relative, expected in manifest["scientific_source_hashes"].items():
        source = root / relative
        if not source.is_file() or sha256(source) != expected:
            raise SystemExit(f"Scientific source mismatch: {relative}")
    dest = args.output.resolve()
    dest.mkdir(parents=True, exist_ok=True)
    for key in keys:
        if key.startswith("FigS"):
            stem = "FigS07_Diagnostics" if key == "FigS07" else "FigS08_PredictorEffects"
            record = manifest["supplementary_figures"][key]
            files = [(root / "figures" / f"{stem}.svg", record["svg_sha256"]),
                     (root / "figures" / f"{stem}.png", record["png_sha256"])]
        else:
            record = manifest["figures"][key]
            files = [(root / record["path"], record["sha256"])]
        for source, expected in files:
            if not source.is_file() or sha256(source) != expected:
                raise SystemExit(f"Publication asset mismatch: {source.name}")
            target = dest / source.name
            if source.resolve() == target:
                raise SystemExit("Output must differ from the source directory")
            shutil.copyfile(source, target)
            if sha256(target) != expected:
                raise SystemExit(f"Export mismatch: {target.name}")
        print(f"{key}: validated and exported")

if __name__ == "__main__":
    main()
