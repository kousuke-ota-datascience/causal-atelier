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


def test_frontend_generates_idempotency_keys_without_requiring_random_uuid() -> None:
    javascript = (REPOSITORY / "frontend" / "app.js").read_text(encoding="utf-8")

    assert "function idempotencyKey()" in javascript
    assert 'typeof globalThis.crypto?.randomUUID==="function"' in javascript
    assert 'typeof globalThis.crypto?.getRandomValues==="function"' in javascript
    assert javascript.count("randomUUID()") == 1
    assert javascript.count("'Idempotency-Key':idempotencyKey()") == 4
