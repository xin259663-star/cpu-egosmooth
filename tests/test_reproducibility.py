
from pathlib import Path
import pandas as pd
def test_formal_run_matrix():
    f=pd.read_csv(Path("results/summary/formal_runs_summary.csv")); assert len(f)==50; assert f.model.nunique()==5; assert set(f.seed)==set(range(10)); assert (f.groupby("model").size()==10).all()
def test_primary_means_tolerance():
    f=pd.read_csv(Path("results/summary/formal_runs_summary.csv")); assert abs(f.raw_ade.mean()-0.8019032841465917)<1e-5; assert abs(f.raw_fde.mean()-1.7214446197749231)<1e-5
