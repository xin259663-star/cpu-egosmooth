
import numpy as np
from egosmooth.metrics import ade_fde, jerk_decomposition
def test_ade_fde_exact():
    gt=np.zeros((2,6,2)); pred=np.ones((2,6,2)); ade,fde=ade_fde(pred,gt); np.testing.assert_allclose(ade,np.sqrt(2)); np.testing.assert_allclose(fde,np.sqrt(2))
def test_trajectory_shapes():
    h=np.zeros((3,4,2)); f=np.zeros((3,6,2)); assert jerk_decomposition(h,f)["terms"].shape==(3,6)
