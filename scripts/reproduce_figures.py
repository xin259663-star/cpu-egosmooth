"""Validate and export locked CEP publication figures; no experiment is rerun."""
from __future__ import annotations
import argparse, hashlib, json, shutil
from pathlib import Path

CURRENT = tuple(f"Fig{i:02d}" for i in range(1, 7)) + ("FigS07", "FigS08")

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--fig", default="all")
    p.add_argument("--root", type=Path, default=Path("."))
    p.add_argument("--output", type=Path)
    a = p.parse_args()
    root = a.root.resolve()
    manifest = json.loads((root / "figures/manifest_cep.json").read_text(encoding="utf-8"))
    keys = CURRENT if a.fig.lower() == "all" else (f"Fig{int(a.fig):02d}",) if a.fig.isdigit() else (a.fig,)
    if not all(key in CURRENT for key in keys):
        p.error("Current set: Fig01-Fig06, FigS07, FigS08")
    for item in manifest["source_assets"]:
        path = root / item["path"]
        if sha(path) != item["sha256"]:
            raise SystemExit(f"Source mismatch: {path}")
    dest_dir = (a.output or root / "figures/reproduced").resolve()
    dest_dir.mkdir(parents=True, exist_ok=True)
    for key in keys:
        for item in manifest["figures"][key]["assets"]:
            source = root / item["path"]
            if sha(source) != item["sha256"]:
                raise SystemExit(f"Locked artwork mismatch: {source}")
            dest = dest_dir / source.name
            if source.resolve() == dest:
                raise SystemExit("Output directory must differ from source directory")
            shutil.copyfile(source, dest)
            if sha(dest) != item["sha256"]:
                raise SystemExit(f"Export mismatch: {dest}")
        print(f"{key}: locked SVG/PNG exported and verified")

if __name__ == "__main__":
    main()
