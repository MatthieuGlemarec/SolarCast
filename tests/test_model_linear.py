from Src.features import add_calendar_features, build_feature_matrices
from Src.modeling import fit_poly_linear, evaluate

def test_poly_linear_trains_and_evaluates(tiny_df):
    out = add_calendar_features(tiny_df, "date")
    out["solargen_scaled"] = out["solargen"]
    X_lin, _, y = build_feature_matrices(out)
    model = fit_poly_linear(X_lin, y)
    metrics = evaluate(model, X_lin, y)
    assert set(metrics) == {"r2","rmse","mae","n"}
    assert metrics["n"] == len(y)
