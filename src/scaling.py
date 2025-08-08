import numpy as np
import pandas as pd

def capacity_scale_to_ref(df: pd.DataFrame, target_col: str, date_col: str, ref_year: int, q: float = 0.95):
    out = df.copy()
    out['year'] = pd.to_datetime(out[date_col]).dt.year
    p95 = out.groupby('year')[target_col].quantile(q)
    if ref_year not in p95.index:
        raise ValueError("Reference year not present in data.")
    ref = p95.loc[ref_year]
    factors = p95.apply(lambda x: ref / x if x != 0 else np.nan)
    if factors.isna().any():
        raise ValueError("Zero/NaN percentile encountered while computing scaling factors.")
    out[target_col + '_scaled'] = out.apply(
        lambda r: r[target_col] * factors.loc[r['year']],
        axis=1
    )
    return out, factors
