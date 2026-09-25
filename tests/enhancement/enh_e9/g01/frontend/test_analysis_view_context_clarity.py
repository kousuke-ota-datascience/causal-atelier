"""Focused ENH-E9 G01 coverage for saved-view and context-selection clarity."""

from pathlib import Path


def _repository_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").is_file():
            return parent
    raise RuntimeError("repository root not found")


REPOSITORY = _repository_root()


def test_saved_analysis_view_has_explicit_read_only_display_action() -> None:
    html = (REPOSITORY / "frontend" / "index.html").read_text(encoding="utf-8")
    app = (REPOSITORY / "frontend" / "app.js").read_text(encoding="utf-8")

    assert 'id="analysis-view-details-modal"' in html
    assert "この表示はread-onlyです" in html
    assert 'onclick="showAnalysisView(' in app
    assert "window.showAnalysisView=async id=>" in app
    assert "/analysis-views/${id}`)" in app
    assert "View specification" in app
    assert "Materialization manifest" in app


def test_saved_analysis_view_display_is_read_only_and_context_selection_is_explained() -> None:
    html = (REPOSITORY / "frontend" / "index.html").read_text(encoding="utf-8")
    app = (REPOSITORY / "frontend" / "app.js").read_text(encoding="utf-8")

    display_handler = app[
        app.index("window.showAnalysisView=async id=>") : app.index("$('#close-analysis-view-details').onclick")
    ]
    assert "method:" not in display_handler
    assert "data-tooltip=\"このProjectで現在の分析に適用する" in html
    assert "Contextの内容や他のresourceを変更しません" in html
