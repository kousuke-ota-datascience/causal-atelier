from pathlib import Path


REPOSITORY = Path(__file__).parents[2]


def _sources() -> tuple[str, str]:
    return (
        (REPOSITORY / "frontend" / "index.html").read_text(encoding="utf-8"),
        (REPOSITORY / "frontend" / "app.js").read_text(encoding="utf-8"),
    )


def test_predictive_workspace_exposes_complete_g5_backend_vertical_slice() -> None:
    html, javascript = _sources()
    predictive = html.split('<section id="predictive"', 1)[1].split(
        '<section id="results"', 1
    )[0]

    assert 'data-workspace="predictive" data-route="predictive"' in html
    assert all(value in predictive for value in (
        'id="predictive-form"',
        'id="predictive-context"',
        'id="predictive-view"',
        'name="task_type"',
        'name="target"',
        'name="feature_columns"',
        'name="split_strategy"',
        'id="run-predictive" disabled',
        'id="predictive-split-validation"',
        'id="predictive-executions"',
        'id="predictive-results"',
        'id="predictive-artifacts"',
    ))
    assert all(value in javascript for value in (
        "/predictive/capabilities",
        "/research-contexts",
        "/analysis-specifications",
        "/execution-plans",
        "/executions",
        "waitForPredictive",
        "data-predictive-specification",
        "Research Context:",
        "Dataset Version:",
        "PREDICTIVE_EXPLANATION_RESULT",
        "MODEL_CARD_RESULT",
    ))
    assert "/predictive/split-validations" not in javascript
    assert "Execution Plan validated" in javascript
    assert "backendAvailable=state.predictiveCapabilities?.training_available===true" in javascript
    assert "state.predictiveCapabilities?.explanation_available===true" in javascript
    assert "state.predictiveCapabilities?.model_card_available===true" in javascript


def test_predictive_terminology_is_explicitly_non_causal() -> None:
    html, javascript = _sources()
    predictive = html.split('<section id="predictive"', 1)[1].split(
        '<section id="results"', 1
    )[0]

    assert "Predictive Explanation ≠ Causal Explanation ≠ Treatment Effect" in predictive
    assert "特徴量の寄与や重要度は予測modelの挙動を説明" in predictive
    assert "因果関係または介入効果を示しません" in predictive
    assert "Predictive Explanation、Model Cardを保存しました" in javascript
    assert "single score" not in predictive.lower()
    assert "rank against causal" not in predictive.lower()


def test_project_shell_recognizes_six_routes_and_restores_predictive_deep_links() -> None:
    html, javascript = _sources()
    routes = ("context", "data", "explore", "causal", "predictive", "results")

    assert all(f'data-route="{route}"' in html for route in routes)
    assert all(f"{route}:'{route}'" in javascript for route in routes)
    assert "history.pushState" in javascript
    assert "window.addEventListener('popstate'" in javascript
    assert "async function restoreProjectRoute()" in javascript
    assert "(context|data|explore|causal|predictive|results)" in javascript
    assert "await loadProjects();await restoreProjectRoute()" in javascript
