from pathlib import Path


def test_navigation_shell_is_catalog_driven_and_uses_operation_availability() -> None:
    repository = Path(__file__).parents[2]
    html = (repository / "frontend/index.html").read_text(encoding="utf-8")
    javascript = (repository / "frontend/app.js").read_text(encoding="utf-8")
    assert 'id="analysis-family-tabs"' in html
    assert 'id="analysis-stage-sidebar"' in html
    assert "catalog.families.map" in javascript
    assert "current.stages.slice().sort((a,b)=>a.order-b.order)" in javascript
    assert "/operation-availability?" in javascript
    assert "NAVIGATION_ASYNC_STATES=Object.freeze(['IDLE','LOADING','READY','EMPTY','PARTIAL','ERROR','CANCELLED'])" in javascript


def test_operation_availability_projection_has_closed_operation_keys() -> None:
    repository = Path(__file__).parents[2]
    source = (repository / "src/ariadne/product/application/product_closure_service.py").read_text(encoding="utf-8")
    assert 'keys = ("RUN", "EDIT", "EXPORT")' in source
    assert 'supported_types = {"analysis-specification", "execution", "result", "graph-version"}' in source
