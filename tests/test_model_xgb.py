from Src.features import add_calendar_features, build_feature_matrices
from Src.modeling import build_xgb_model, evaluate

def test_xgb_trains_and_evaluates(tiny_df):
    out = add_calendar_features(tiny_df, "date")
    out["solargen_scaled"] = out["solargen"]
    _, X_xgb, y = build_feature_matrices(out)
    model = build_xgb_model()
    model.fit(X_xgb, y)
    metrics = evaluate(model, X_xgb, y)
    assert metrics["n"] == len(y)
