import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parents[5]
RUNNER = ROOT / "tests/enhancement/enh_e10/g03/browser_e2e/run_predictive_advanced.py"


def test_advanced_browser_runner_materializes_both_frozen_journeys() -> None:
    source = RUNNER.read_text(encoding="utf-8")
    ast.parse(source)
    for required in (
        "lightgbm_classifier.v1", "SHAP_TREE", "lightgbm_regressor.v1",
        "LIME_TABULAR", "PREDICTIVE_EXPLANATION_RESULT", "MODEL_CARD_RESULT",
        "PREDICTIVE_EXPLANATION", "MODEL_CARD", "FITTED_MODEL",
        "context.tracing.start", "failure.png", "evidence.json", "def _wait(",
    ):
        assert required in source


def test_advanced_compose_and_browser_image_are_hermetic() -> None:
    compose = (ROOT / "compose.enh_e10.yaml").read_text(encoding="utf-8")
    dockerfile = (ROOT / "Dockerfile.browser-e2e").read_text(encoding="utf-8")
    advanced = (ROOT / "Dockerfile.predictive-advanced").read_text(encoding="utf-8")
    dockerignore = (ROOT / ".dockerignore").read_text(encoding="utf-8")
    assert "Dockerfile.predictive-advanced" in compose
    assert "predictive-advanced" in advanced
    assert "run_predictive_advanced.py" in dockerfile
    assert "!tests/enhancement/enh_e10/g03/browser_e2e/run_predictive_advanced.py" in dockerignore
