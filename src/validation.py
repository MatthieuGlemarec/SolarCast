import numpy as np
import pandas as pd

REQUIRED = ["date", "glorad", "rain", "maxtp", "mintp", "solargen"]

def basic_schema_check(df: pd.DataFrame):
    """Light defensive checks for incorrect or adversarial input."""
    missing = [c for c in REQUIRED if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    if df["date"].isna().any():
        raise ValueError("Invalid dates (NaT) detected.")
    num = df.select_dtypes(include="number")
    if not np.isfinite(num.values).all():
        raise ValueError("Non-finite numeric values detected (NaN/Inf).")
    return True
