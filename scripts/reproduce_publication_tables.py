"""Export current Table 5 and historical timing sensitivity from saved data."""
from __future__ import annotations
import argparse,csv
from pathlib import Path
def read(path):
    with path.open(encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
def write(path,fields,rows):
    with path.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root",type=Path,default=Path("."));p.add_argument("--output",type=Path)
    a=p.parse_args();root=a.root.resolve();out=a.output or root/"results/tables/reproduced_v6";out.mkdir(parents=True,exist_ok=True)
    timing=read(root/"results/figure_data/fig07_timestamp_sensitivity.csv");rows=[]
    for label,definition in [("Nominal 0.5-s grid","nominal_0.5_s"),("Exact timestamps","exact_timestamps")]:
        block=[r for r in timing if r["timing_definition"]==definition]
        fixed=float(next(r["relative_reduction_percent"] for r in block if r["comparison"].startswith("Fixed")))
        selected=float(next(r["relative_reduction_percent"] for r in block if r["comparison"].startswith("Validation")))
        rows.append({"Timing definition":label,"Fixed SG − Raw":f"{fixed:.1f}%","Selected − Raw":f"{selected:.1f}%","Difference":f"{selected-fixed:+.1f} pp"})
    assert [list(r.values())[1:] for r in rows]==[["44.3%","46.3%","+2.0 pp"],["23.5%","24.7%","+1.2 pp"]]
    write(out/"Supplementary_timing_sensitivity.csv",list(rows[0]),rows)
    controls=read(root/"results/figure_data/fig08_kinematic_controls.csv");rows=[]
    for code,label in [("Neural overall","Neural Raw"),("CV","CV"),("CA","CA"),("CTRV","CTRV")]:
        r=next(r for r in controls if r["method"]==code and r["strategy"]=="Raw");shape=float(r["history_aware_mean_geometric_jerk"])
        rows.append({"Control":label,"ADE (m)":f"{float(r['ADE']):.4f}","FDE (m)":f"{float(r['FDE']):.4f}","Shape (m s⁻³)":"0" if shape==0 else f"{shape:.3f}"})
    assert [list(r.values())[1:] for r in rows]==[["0.8019","1.7214","1.878"],["1.2467","2.6035","0.275"],["1.8183","4.0561","0"],["1.0786","2.3398","0.436"]]
    write(out/"Table05_kinematic_controls.csv",list(rows[0]),rows)
    print("Current Table 5 and historical timing sensitivity exported from unchanged sources")
if __name__=="__main__":main()
