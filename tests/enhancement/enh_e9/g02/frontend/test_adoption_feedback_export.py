"""Focused ENH-E9 G02 P03 coverage for modal feedback and Mermaid export."""

from pathlib import Path


def _repository_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").is_file():
            return parent
    raise RuntimeError("repository root not found")


REPOSITORY = _repository_root()


def test_adoption_feedback_is_local_to_the_graph_modal_and_uses_returned_graph_identity() -> None:
    html = (REPOSITORY / "frontend" / "index.html").read_text(encoding="utf-8")
    app = (REPOSITORY / "frontend" / "app.js").read_text(encoding="utf-8")
    adoption = app[app.index("$('#adopt-graph').onclick") : app.index("$('#save-direct-graph').onclick")]

    assert 'id="graph-modal-feedback"' in html
    assert "setGraphModalFeedback" in app
    assert "graph.graph_version_id,{preserveFeedback:true}" in adoption
    assert "graph.graph_version_id" in adoption
    assert "graph.status" in adoption


def test_mermaid_export_is_a_deterministic_projection_without_graph_mutation() -> None:
    html = (REPOSITORY / "frontend" / "index.html").read_text(encoding="utf-8")
    app = (REPOSITORY / "frontend" / "app.js").read_text(encoding="utf-8")
    export_handler = app[app.index("$('#export-graph-mermaid').onclick") : app.index("async function comparisonExecutionMetadata")]
    mermaid = app[app.index("function mermaidMarkdownSource") : app.index("window.inspectCandidate=inspectCandidate")]

    assert 'id="export-graph-mermaid"' in html
    assert 'id="graph-mermaid-source"' in html
    assert "flowchart LR" in mermaid
    assert ".sort(" in mermaid
    assert "endpoint_source" in mermaid and "endpoint_target" in mermaid
    assert "candidate?.graph" in export_handler
    assert "new Blob" in export_handler
    assert "api(" not in export_handler
    assert "fetch(" not in export_handler
