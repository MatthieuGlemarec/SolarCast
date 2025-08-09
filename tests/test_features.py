from Src.features import add_calendar_features, build_feature_matrices

def test_add_calendar_features_ok(tiny_df):
    out = add_calendar_features(tiny_df, "date")
    for c in ["month","dayofyear","sin_doy","cos_doy"]:
        assert c in out.columns

def test_build_feature_matrices_ok(tiny_df):
    out = add_calendar_features(tiny_df, "date")
    out["solargen_scaled"] = out["solargen"]  # mimic scaled target for test
    X_lin, X_xgb, y = build_feature_matrices(out)
    assert {"glorad","maxtp","rain","glorad_sq"}.issubset(set(X_lin.columns))
    assert len(X_xgb) == len(y)
