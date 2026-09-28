"""Validate saved summaries and export locked v7.1 SVG/PNG; no experiments rerun.

This is frozen-artwork export, not regeneration of trajectories from raw data.
Source checks validate displayed counts and the locked Fig.3 case independently.
"""
from __future__ import annotations
import argparse,csv,hashlib,json,shutil
from pathlib import Path
CURRENT=tuple(range(1,7))+("S07",)
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def rows(path):
    with path.open(encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
def validate_data(root):
    d=root/"results/figure_data"
    data=rows(d/"fig07_selection_sensitivity.csv")
    for eps,near,retained in [(0,3,50),(.001,6,40),(.005,6,35)]:
        block=[r for r in data if float(r["epsilon"])==eps]
        assert len(block)==50
        assert sum(r["near_tie"].lower()=="true" for r in block)==near
        assert sum(r["same_as_epsilon0"].lower()=="true" for r in block)==retained
    cases=rows(d/"fig3_selected_cases.csv")
    case=next(r for r in cases if r["panel"]=="b")
    assert case["scene_token"]=="b0b26c1e5a1140e69598422f12ae1dc0"
    assert case["sample_token"]=="53a3b6ba49af484d9d0bab0ffb9dea01"
    assert case["log_token"]=="7a0fde44c3504eaeb18f9ad83bed65bc"
    assert case["window_index"]=="19"
    assert all(r["run_id"]=="P2B_042_log_primary_PositionalTransformer_s1" and r["seed"]=="1" for r in cases)
    for name in ["figS07_aggregation_summary.csv","figS07_lolo_effects.csv","figS07_internal_configuration.csv"]:
        assert (d/name).is_file()
def reproduce(n,root,output=None):
    if n not in CURRENT:raise ValueError("Current figures: 01–06 and S07. Former Fig07 is merged into Fig06(c); Fig08 is superseded by Table 6 and Methods 2.6.")
    manifest=json.loads((root/"figures/manifest_v7_1.json").read_text(encoding="utf-8"))
    key="FigS07" if n=="S07" else f"Fig{n:02d}"
    target=output or root/"figures/reproduced"
    target.mkdir(parents=True,exist_ok=True)
    for asset in manifest["figures"][key]["assets"]:
        source=root/asset["path"]
        assert sha(source)==asset["sha256"],f"Locked asset mismatch: {source.name}"
        dest=target/source.name
        if dest.resolve()==source.resolve():raise ValueError("Output must differ from locked source directory")
        shutil.copyfile(source,dest)
        assert sha(dest)==asset["sha256"]
    print(f"{key}: locked SVG/PNG exported; source-data checks passed")
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--fig",default="all");p.add_argument("--root",type=Path,default=Path("."));p.add_argument("--output",type=Path)
    a=p.parse_args();root=a.root.resolve();validate_data(root)
    nums=CURRENT if a.fig=="all" else ("S07",) if a.fig.upper()=="S07" else (int(a.fig),)
    for n in nums:reproduce(n,root,a.output)
if __name__=="__main__":main()
