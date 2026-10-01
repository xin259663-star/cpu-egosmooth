from pathlib import Path
import json,hashlib

ROOT=Path(__file__).resolve().parents[1]
def test_archived_fig1_icon_sources_are_original_tabler_outline():
    manifest=json.loads((ROOT/'figures/archive/pre_cep/manifest_v7_1.json').read_text(encoding='utf-8'))
    sources=manifest['Fig01_icon_sources']
    assert sources['official_repository']=='tabler/tabler-icons'
    assert sources['path_modified'] is False
    assert len(sources['sources'])==5
    for item in sources['sources']:
        raw=(ROOT/item['path']).read_bytes()
        assert hashlib.sha256(raw).hexdigest()==item['sha256']
    license_bytes=(ROOT/sources['license_path']).read_bytes()
    assert hashlib.sha256(license_bytes).hexdigest()==sources['license_sha256']
