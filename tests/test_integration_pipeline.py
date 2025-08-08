from src.scaling import capacity_scale_to_ref
from src.features import add_calendar_features
from src.modeling import fit_poly_linear

def test_pipeline_end_to_end(sample_df):
    df_scaled, _ = capacity_scale_to_ref(sample_df, "solargen", "date", 2024)
    df_features = add_calendar_features(df_scaled, "date")
    model = fit_poly_linear(df_features, df_features["solargen_scaled"])
    assert hasattr(model, "predict")
