from sklearn.model_selection import train_test_split
from Src.validation import basic_schema_check
from Src.scaling import capacity_scale_to_ref
from Src.features import add_calendar_features, build_feature_matrices
from Src.modeling import build_xgb_model, evaluate

def test_full_pipeline_end_to_end(tiny_df):
    assert basic_schema_check(tiny_df)
    scaled, _ = capacity_scale_to_ref(tiny_df, "solargen", "date", 2024)
    fe = add_calendar_features(scaled, "date")
    X_lin, X_xgb, y = build_feature_matrices(fe)
    Xtr, Xte, ytr, yte = train_test_split(X_xgb, y, test_size=0.2, random_state=42)
    model = build_xgb_model()
    model.fit(Xtr, ytr)
    m_train = evaluate(model, Xtr, ytr)
    m_test = evaluate(model, Xte, yte)
    assert m_train["rmse"] >= 0 and m_test["rmse"] >= 0
