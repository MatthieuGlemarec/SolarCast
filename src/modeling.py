import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
import xgboost as xgb

def fit_poly_linear(X_train: pd.DataFrame, y_train: pd.Series) -> LinearRegression:
    """Fit OLS on polynomial linear features (expects glorad, maxtp, rain, glorad_sq)."""
    model = LinearRegression()
    model.fit(X_train, y_train)
    return model

def build_xgb_model() -> xgb.XGBRegressor:
    """Return tuned XGBRegressor aligned with XGBoost 2023-2025 notebook."""
    return xgb.XGBRegressor(
        learning_rate=0.1,
        max_depth=4,
        n_estimators=400,
        reg_alpha=0.5,
        reg_lambda=1.0,
        min_child_weight=11,
        random_state=42,
        n_jobs=-1
    )

def evaluate(model, X: pd.DataFrame, y: pd.Series) -> dict:
    """Return standard metrics for convenience."""
    pred = model.predict(X)
    rmse = float(np.sqrt(mean_squared_error(y, pred)))
    return {
        "r2": float(r2_score(y, pred)),
        "rmse": rmse,
        "mae": float(mean_absolute_error(y, pred)),
        "n": int(len(y)),
    }
