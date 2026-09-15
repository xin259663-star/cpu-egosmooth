from pathlib import Path

import yaml


def test_citation_cff_has_required_software_fields():
    citation = yaml.safe_load(Path("CITATION.cff").read_text(encoding="utf-8"))
    assert citation["cff-version"] == "1.2.0"
    assert citation["type"] == "software"
    assert citation["version"] == "1.0.0"
    assert citation["title"] == (
        "Accuracy-Constrained Evaluation of Geometric Effects in Short-Horizon "
        "Open-Loop Ego-Trajectory Post-Processing"
    )
    assert citation["authors"] == [
        {
            "family-names": "Zhu",
            "given-names": "Kexin",
            "orcid": "https://orcid.org/0009-0004-7456-9491",
        },
        {
            "family-names": "Xu",
            "given-names": "Xu",
            "orcid": "https://orcid.org/0000-0003-3602-1391",
        },
    ]
