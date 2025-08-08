from src.modeling import build_xgb

def test_build_xgb():
    model = build_xgb()
    assert hasattr(model, "fit")
