from pathlib import Path
import csv
import hashlib
import json
import subprocess
import sys

import pytest


ROOT = Path(__file__).resolve().parents[1]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_current_locked_assets():
    manifest = json.loads((ROOT / "manifest_current.json").read_text(encoding="utf-8"))
    assert set(manifest["figures"]) == {f"Fig{i:02d}" for i in range(1, 6)}
    assert set(manifest["supplementary_figures"]) == {"FigS07", "FigS08"}
    for item in manifest["figures"].values():
        assert sha256(ROOT / item["path"]) == item["sha256"]
    stems = {"FigS07": "FigS07_Diagnostics", "FigS08": "FigS08_PredictorEffects"}
    for key, stem in stems.items():
        record = manifest["supplementary_figures"][key]
        assert sha256(ROOT / "figures" / f"{stem}.svg") == record["svg_sha256"]
        assert sha256(ROOT / "figures" / f"{stem}.png") == record["png_sha256"]


def test_export_current_collection(tmp_path):
    completed = subprocess.run(
        [sys.executable, str(ROOT / "scripts/reproduce_figures.py"), "--root", str(ROOT), "--fig", "all", "--output", str(tmp_path)],
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, completed.stderr
    assert len(list(tmp_path.iterdir())) == 9
    assert (tmp_path / "FigS08_PredictorEffects.svg").is_file()


@pytest.mark.parametrize("name", ["Fig06", "Fig07", "Fig08"])
def test_export_rejects_superseded_numbered_figures(tmp_path, name):
    completed = subprocess.run(
        [sys.executable, str(ROOT / "scripts/reproduce_figures.py"), "--root", str(ROOT), "--fig", name, "--output", str(tmp_path)],
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode != 0


def test_table_source_hashes():
    manifest = json.loads((ROOT / "manifest_current.json").read_text(encoding="utf-8"))
    for relative, expected in manifest["table_source_hashes"].items():
        assert sha256(ROOT / relative) == expected
    for name, count in [("Table05_timing_sensitivity.csv", 2), ("Table06_kinematic_controls.csv", 4)]:
        with (ROOT / "results/tables" / name).open(encoding="utf-8", newline="") as handle:
            assert len(list(csv.DictReader(handle))) == count
