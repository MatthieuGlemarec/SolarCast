from src.features import add_calendar_features

def test_add_calendar_features(sample_df):
    df_feat = add_calendar_features(sample_df, "date")
    for col in ["month", "dayofyear", "sin_doy", "cos_doy"]:
        assert col in df_feat.columns
