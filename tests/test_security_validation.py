import pandas as pd
import pytest
from src.scaling import capacity_scale_to_ref

def test_invalid_ref_year(sample_df):
    with pytest.raises(ValueError):
        capacity_scale_to_ref(sample_df, "solargen", "date", 1999)
