import pytest
import pandas as pd
import numpy as np

@pytest.fixture
def tiny_df():
    # small 2 year sample
    dates = pd.date_range("2024-05-01", periods=12, freq="7D").tolist() + \
            pd.date_range("2025-05-01", periods=12, freq="7D").tolist()
    n = len(dates)
    return pd.DataFrame({
        "date": dates,
        "glorad": np.linspace(800, 1400, n),
        "rain": np.linspace(0, 10, n),
        "maxtp": np.linspace(8, 24, n),
        "mintp": np.linspace(2, 14, n),
        "solargen": np.linspace(5000, 15000, n)
    })
