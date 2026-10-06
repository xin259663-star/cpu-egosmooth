from pathlib import Path
import json,hashlib
import xml.etree.ElementTree as E

ROOT=Path(__file__).resolve().parents[1]
def test_fig1_icons_are_original_tabler_outline():
    archive=ROOT/'figures/archive/superseded_v7_3'
    manifest=json.loads((archive/'manifest_v7_1.json').read_text(encoding='utf-8'))
    sources=manifest['Fig01_icon_sources']
    assert sources['official_repository']=='tabler/tabler-icons'
    assert sources['path_modified'] is False
    figure=E.parse(archive/'Fig01.svg').getroot()
    icons=figure.findall('{http://www.w3.org/2000/svg}svg')
    assert len(icons)==len(sources['sources'])==5
    for icon,item in zip(icons,sources['sources']):
        raw=(ROOT/item['path']).read_bytes()
        assert hashlib.sha256(raw).hexdigest()==item['sha256']
        original=E.fromstring(raw)
        assert [(c.tag,c.attrib) for c in icon]==[(c.tag,c.attrib) for c in original]
        assert icon.attrib['viewBox']=='0 0 24 24'
        assert icon.attrib['stroke-width']=='2'
        assert icon.attrib['fill']=='none' and icon.attrib['stroke']=='currentColor'
        assert icon.attrib['data-tabler-icon']==item['name']
    license_bytes=(ROOT/sources['license_path']).read_bytes()
    assert hashlib.sha256(license_bytes).hexdigest()==sources['license_sha256']
