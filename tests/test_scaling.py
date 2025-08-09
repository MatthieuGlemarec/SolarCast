import numpy as np
from Src.scaling import capacity_scale_to_ref

def test_capacity_scale_p95_equalized(tiny_df):
    out, _ = capacity_scale_to_ref(tiny_df, target_col="solargen", date_col="date", ref_year=2024, q=0.95)
    p = out.groupby("year")["solargen_scaled"].quantile(0.95)
    assert np.isclose(p.loc[2024], p.loc[2025], rtol=0.02)
