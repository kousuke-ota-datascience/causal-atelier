"""Focused ENH-E9 G02 P02 coverage for selection and comparison clarity."""

from pathlib import Path


REPOSITORY = Path(__file__).parents[2]


def test_graph_candidate_selection_controls_only_update_selection_state() -> None:
    html = (REPOSITORY / "frontend" / "index.html").read_text(encoding="utf-8")
    app = (REPOSITORY / "frontend" / "app.js").read_text(encoding="utf-8")
    handlers = app[app.index("function updateGraphCandidateSelection()") : app.index("$('#compare-discovery').onclick")]

    assert 'id="select-all-graph-candidates"' in html
    assert 'id="clear-graph-candidates"' in html
    assert "item.checked=selected" in handlers
    assert "updateGraphCandidateSelection()" in handlers
    assert "api(" not in handlers
    assert "adopt" not in handlers.lower()
    assert "fix" not in handlers.lower()


def test_current_comparison_highlight_and_algorithm_summary_use_persisted_data() -> None:
    app = (REPOSITORY / "frontend" / "app.js").read_text(encoding="utf-8")
    css = (REPOSITORY / "frontend" / "styles.css").read_text(encoding="utf-8")
    service = (REPOSITORY / "src/ariadne/interfaces/web_api/routers/executions.py").read_text(encoding="utf-8")

    assert "current-comparison-candidate" in app
    assert "aria-current" in app
    assert "Current comparison candidate" in app
    assert "/prefill`" in app
    assert "metadata.parameters" in app
    assert '@router.get("/executions/{execution_id}/prefill"' in service
    assert "#comparison-tabs button.current-comparison-candidate" in css
