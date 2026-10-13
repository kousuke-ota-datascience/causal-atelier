from pathlib import Path


REPOSITORY = Path(__file__).parents[2]


def test_p02_explainability_and_model_management_remain_capability_and_read_driven() -> None:
    html = (REPOSITORY / "frontend" / "index.html").read_text(encoding="utf-8")
    app = (REPOSITORY / "frontend" / "app.js").read_text(encoding="utf-8")

    assert 'id="predictive-explanation-status"' in html
    assert "function renderPredictiveExplanationControls()" in app
    assert "model_explanation_compatibility" in app
    assert "supports_global" in app and "supports_local" in app
    assert "unavailable:" in app
    assert "function predictiveExplanationReadView" in app
    assert "function predictiveModelManagementReadView" in app
    assert "Model Card (read-only)" in app
    assert "Predictive Explanation ≠ Causal Explanation ≠ Treatment Effect" in html
