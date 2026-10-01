from __future__ import annotations

import csv
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = json.loads((ROOT / 'figures/manifest_cep.json').read_text(encoding='utf-8'))
CURRENT = {f'Fig{i:02d}' for i in range(1, 7)} | {'FigS07', 'FigS08'}


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_current_locked_assets_and_sources():
    assert set(MANIFEST['figures']) == CURRENT
    for item in list(MANIFEST['source_assets']) + [
        asset for figure in MANIFEST['figures'].values() for asset in figure['assets']
    ]:
        path = ROOT / item['path']
        assert path.is_file()
        assert _sha(path) == item['sha256']
        assert path.stat().st_size == item['bytes']


def test_current_export(tmp_path):
    subprocess.run(
        [sys.executable, str(ROOT / 'scripts/reproduce_figures.py'), '--fig', 'all',
         '--root', str(ROOT), '--output', str(tmp_path)],
        check=True, capture_output=True, text=True,
    )
    assert len(list(tmp_path.iterdir())) == 16
    assert not list(tmp_path.glob('Fig07*'))
    assert not list(tmp_path.glob('Fig08*'))


def test_old_main_figures_are_archived():
    assert not (ROOT / 'figures/Fig07.svg').exists()
    assert not (ROOT / 'figures/Fig08.svg').exists()
    assert (ROOT / 'figures/archive/pre_cep/reproduced/Fig07.png').is_file()
    assert (ROOT / 'figures/archive/pre_cep/reproduced/Fig08.png').is_file()


def test_fig3_case_b_and_tables():
    with (ROOT / 'results/figure_data/fig3_selected_cases.csv').open(encoding='utf-8', newline='') as fh:
        rows = list(csv.DictReader(fh))
    assert len(rows) == 4
    assert any(row.get('window_index') == '19' and 'b0b26c1e5a1140e69598422f12ae1dc0' in row.values() for row in rows)
    with (ROOT / 'analysis/Table05_source.csv').open(encoding='utf-8', newline='') as fh:
        assert len(list(csv.DictReader(fh))) == 2
    with (ROOT / 'analysis/Table06_source.csv').open(encoding='utf-8', newline='') as fh:
        assert len(list(csv.DictReader(fh))) == 4
