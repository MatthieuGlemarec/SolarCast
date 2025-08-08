import pytest
import pandas as pd
from src.scaling import capacity_scale_to_ref

def test_capacity_scale_to_ref(sample_df):
    df_scaled, factors = capacity_scale_to_ref(sample_df, "solargen", "date", 2024)
    assert "solargen_scaled" in df_scaled.columns
    assert factors is not None
    assert len(factors) >= 1
