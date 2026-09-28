from pathlib import Path
import hashlib,json,csv,importlib.util
ROOT=Path(__file__).resolve().parents[1]
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
def test_current_locked_assets():
    manifest=json.loads((ROOT/'figures/manifest_v6.json').read_text(encoding='utf-8'))
    assert set(manifest['figures'])=={f'Fig{i:02d}' for i in range(1,8)}|{'FigS07'}
    for item in manifest['figures'].values():
        for a in item['assets']:
            assert hashlib.sha256((ROOT/a['path']).read_bytes()).hexdigest()==a['sha256']
def test_export_current_collection(tmp_path):
    m=load('export_v6',ROOT/'scripts/reproduce_figures.py');m.validate_data(ROOT)
    for n in m.CURRENT:m.reproduce(n,ROOT,tmp_path)
    assert len(list(tmp_path.iterdir()))==16
    assert not list(tmp_path.glob('Fig08*'))
def test_export_rejects_old_fig8(tmp_path):
    import pytest
    m=load('export_v6_reject',ROOT/'scripts/reproduce_figures.py')
    with pytest.raises(ValueError):m.reproduce(8,ROOT,tmp_path)
def test_table_source_hashes():
    m=json.loads((ROOT/'figures/manifest_v6.json').read_text(encoding='utf-8'))
    for t in m['tables'].values():
        assert hashlib.sha256((ROOT/t['source']).read_bytes().replace(b'\r\n',b'\n')).hexdigest()==t['source_sha256']
    for name,count in [('Table05_timing_sensitivity.csv',2),('Table06_kinematic_controls.csv',4)]:
        with (ROOT/'results/tables'/name).open(encoding='utf-8',newline='') as f:assert len(list(csv.DictReader(f)))==count
