import pandas as pd
from src.modeling import fit_poly_linear, evaluate

def test_fit_poly_linear(sample_df):
    model = fit_poly_linear(sample_df, sample_df["solargen"])
    assert hasattr(model, "predict")

def test_evaluate(sample_df):
    from sklearn.linear_model import LinearRegression
    X = sample_df[['glorad', 'maxtp', 'rain']].copy()
    X['glorad_sq'] = X['glorad'] ** 2
    model = LinearRegression().fit(X, sample_df["solargen"])
    metrics = evaluate(model, X, sample_df["solargen"])
    assert "r2" in metrics and "rmse" in metrics and "mae" in metrics
