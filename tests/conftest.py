import pytest
import pandas as pd
import numpy as np

@pytest.fixture
def sample_df():
    data = {
        "date": pd.date_range("2024-01-01", periods=6, freq="D"),
        "glorad": [100, 200, 150, 180, 210, 190],
        "maxtp": [12, 14, 11, 13, 15, 14],
        "mintp": [5, 6, 4, 5, 7, 6],
        "rain": [0, 5, 2, 0, 1, 3],
        "solargen": [1000, 2000, 1500, 1800, 2200, 2100]
    }
    return pd.DataFrame(data)
