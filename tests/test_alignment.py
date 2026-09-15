
from pathlib import Path
import pandas as pd
def test_test_index_cardinality():
    f=pd.read_csv(Path("results/provenance/test_window_index.csv")); assert len(f)==2901; assert f.scene_token.nunique()==93; assert f.log_token.nunique()==7; assert not f.duplicated(["scene_token","sample_token"]).any()
