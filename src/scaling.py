import numpy as np
import pandas as pd

def capacity_scale_to_ref(
    df: pd.DataFrame,
    target_col: str = "solargen",
    date_col: str = "date",
    ref_year: int = 2024,
    q: float = 0.95,
) -> tuple[pd.DataFrame, pd.Series]:
    """
    Scale daily generation so each year's q-quantile matches the reference year's q-quantile.
    Returns (scaled_df, scaling_factors).
    """
    out = df.copy()
    years = pd.to_datetime(out[date_col], errors="coerce")
    if years.isna().any():
        raise ValueError("Invalid dates encountered during scaling.")
    out["year"] = years.dt.year

    p = out.groupby("year")[target_col].quantile(q)
    if ref_year not in p.index:
        raise ValueError("Reference year not present in data.")
    ref_val = p.loc[ref_year]

    factors = p.apply(lambda v: np.nan if v == 0 else ref_val / v)
    if factors.isna().any():
        raise ValueError("Zero/NaN percentile encountered when computing factors.")

    out[target_col + "_scaled"] = out.apply(
        lambda r: r[target_col] * factors.loc[r["year"]], axis=1
    )
    return out, factors
