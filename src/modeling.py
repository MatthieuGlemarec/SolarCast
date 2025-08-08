import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
import xgboost as xgb

def fit_poly_linear(X_train_df: pd.DataFrame, y_train):
    X_train = X_train_df[['glorad', 'maxtp', 'rain']].copy()
    X_train['glorad_sq'] = X_train_df['glorad'] ** 2
    model = LinearRegression().fit(X_train, y_train)
    return model

def build_xgb():
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

def evaluate(model, X, y):
    yhat = model.predict(X)
    rmse = np.sqrt(mean_squared_error(y, yhat))
    return {
        "r2": r2_score(y, yhat),
        "rmse": rmse,
        "mae": mean_absolute_error(y, yhat),
        "n": len(y)
    }
