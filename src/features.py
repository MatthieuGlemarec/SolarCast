import numpy as np
import pandas as pd

def add_calendar_features(df: pd.DataFrame, date_col: str):
    out = df.copy()
    dt = pd.to_datetime(out[date_col])
    out['month'] = dt.dt.month
    out['dayofyear'] = dt.dt.dayofyear
    out['sin_doy'] = np.sin(2 * np.pi * out['dayofyear'] / 365.0)
    out['cos_doy'] = np.cos(2 * np.pi * out['dayofyear'] / 365.0)
    return out
