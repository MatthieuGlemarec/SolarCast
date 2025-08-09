import numpy as np
import pandas as pd
import pytest
from Src.validation import basic_schema_check

def test_missing_columns_rejected(tiny_df):
    bad = tiny_df.drop(columns=["glorad"])
    with pytest.raises(ValueError):
        basic_schema_check(bad)

def test_nonfinite_rejected(tiny_df):
    bad = tiny_df.copy()
    bad.loc[0, "rain"] = np.inf
    with pytest.raises(ValueError):
        basic_schema_check(bad)

def test_invalid_dates_rejected(tiny_df):
    bad = tiny_df.copy()
    bad.loc[0, "date"] = pd.NaT
    with pytest.raises(ValueError):
        basic_schema_check(bad)
