import numpy as np
import pandas as pd

def add_calendar_features(df: pd.DataFrame, date_col: str = "date") -> pd.DataFrame:
    """Add month/dayofyear and seasonal encodings."""
    out = df.copy()
    dt = pd.to_datetime(out[date_col], errors="coerce")
    if dt.isna().any():
        raise ValueError("Invalid dates encountered while adding calendar features.")
    out["month"] = dt.dt.month
    out["dayofyear"] = dt.dt.dayofyear
    out["sin_doy"] = np.sin(2 * np.pi * out["dayofyear"] / 365.0)
    out["cos_doy"] = np.cos(2 * np.pi * out["dayofyear"] / 365.0)
    return out

def build_feature_matrices(df: pd.DataFrame):
    """
    Return (X_linear_poly, X_xgb, y) using notebooks definitions:
      - Linear poly: glorad, maxtp, rain, glorad^2
      - XGBoost: glorad, maxtp, mintp, rain, month, dayofyear, sin_doy, cos_doy
      - y: solargen_scaled
    """
    if "solargen_scaled" not in df.columns:
        raise ValueError("Expected 'solargen_scaled' in DataFrame.")
    # Linear (polynomial) features
    X_lin = df[["glorad", "maxtp", "rain"]].copy()
    X_lin["glorad_sq"] = df["glorad"] ** 2
    # XGBoost features
    xgb_cols = ["glorad", "maxtp", "mintp", "rain", "month", "dayofyear", "sin_doy", "cos_doy"]
    missing = [c for c in xgb_cols if c not in df.columns]
    if missing:
        raise ValueError(f"Missing XGBoost features: {missing}")
    X_xgb = df[xgb_cols].copy()
    y = df["solargen_scaled"].copy()
    return X_lin, X_xgb, y
