from pathlib import Path


REPOSITORY = Path(__file__).parents[2]


def test_four_workspace_frontend_uses_only_product_api_contract() -> None:
    html = (REPOSITORY / "frontend" / "index.html").read_text(encoding="utf-8")
    javascript = (REPOSITORY / "frontend" / "app.js").read_text(encoding="utf-8")
    assert all(f'id="{workspace}"' in html for workspace in (
        "data", "discovery", "inference", "results",
    ))
    assert 'const API="/api/v1"' in javascript
    assert not any(value in javascript for value in (
        "/api/projects", "/api/executions", "mlflow", "pipeline", "ariadne.legacy",
    ))
    assert all(endpoint in javascript for endpoint in (
        "/dataset-versions", "/execution-batches", "/comparisons/query",
        "/graph-versions", "/annotations", "/lineage", "/artifacts/", "/export",
    ))
    assert "target_graph_version_id:graph.graph_version_id" in javascript
    assert "parent_graph_version_id:parent||null" in javascript
    assert "origin=parent?$('#graph-transform').value:'DISCOVERED'" in javascript
    assert "save-direct-graph" in html and "direct-graph-json" in javascript
    assert all(value in html for value in ("result-type-filter", "result-status-filter"))
    assert "compatible estimators=" in javascript
    assert all(value in html for value in (
        "base-executions", "change_reason", "scientific-warnings",
    ))
    assert all(value in javascript for value in (
        "base_execution_id:base", "change_reason:changeReason",
        "scientific_warnings", "inferred_types",
    ))


def test_frontend_generates_idempotency_keys_without_requiring_random_uuid() -> None:
    javascript = (REPOSITORY / "frontend" / "app.js").read_text(encoding="utf-8")

    assert "function idempotencyKey()" in javascript
    assert 'typeof globalThis.crypto?.randomUUID==="function"' in javascript
    assert 'typeof globalThis.crypto?.getRandomValues==="function"' in javascript
    assert javascript.count("randomUUID()") == 1
    assert javascript.count("'Idempotency-Key':idempotencyKey()") == 8


def test_discovery_form_validates_api_constraints_and_renders_error_details() -> None:
    html = (REPOSITORY / "frontend" / "index.html").read_text(encoding="utf-8")
    javascript = (REPOSITORY / "frontend" / "app.js").read_text(encoding="utf-8")

    assert "function discoveryRequest(form)" in javascript
    assert "Algorithmを1件以上選択してください" in javascript
    assert "PC alphaは0より大きく1より小さい数値" in javascript
    assert "Feature columnsに重複があります" in javascript
    assert "Datasetに存在しないFeature columns" in javascript
    assert "Executionは一度に20件まで" in javascript
    assert "error.details?.errors" in javascript
    assert "item.loc.filter(value=>value!=='body').join('.')" in javascript
    assert 'name="objective" value="Compare candidate causal structures" maxlength="4000"' in html
    assert 'name="rationale" value="Algorithm and PC sensitivity comparison" maxlength="8000"' in html
