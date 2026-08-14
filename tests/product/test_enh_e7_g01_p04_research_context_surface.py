"""Focused ENH-E7 G01 P04 coverage for the Project Context surface."""

import re
from pathlib import Path


REPOSITORY = Path(__file__).parents[2]


def _context_section() -> str:
    html = (REPOSITORY / "frontend" / "index.html").read_text(encoding="utf-8")
    match = re.search(r'<section id="context" class="workspace.*?</section>', html, flags=re.DOTALL)
    assert match is not None
    return match.group(0)


def test_project_context_surface_owns_edit_lifecycle_history_and_related_analysis() -> None:
    section = _context_section()
    app = (REPOSITORY / "frontend" / "app.js").read_text(encoding="utf-8")

    assert 'id="research-context-form"' in section
    assert 'id="update-context"' in section
    assert 'id="fix-context"' in section
    assert 'id="research-context-history"' in section
    assert 'id="research-context-usage"' in section
    assert "context.status==='FIXED'" in app
    assert "/research-contexts/${id}/usage" in app


def test_context_preserves_draft_fixed_lifecycle_and_does_not_create_execution_semantics() -> None:
    app = (REPOSITORY / "frontend" / "app.js").read_text(encoding="utf-8")

    assert "research-contexts/${id}`,{method:'PATCH'" in app
    assert "research-contexts/${id}/fix`,{method:'POST'}" in app
    assert "Research ContextをFIXED化しました。以後は上書きできません" in app
    context_handlers = app[app.index("function contextFormPayload()") : app.index("function predictiveFamilySpec()")]
    assert "/executions" not in context_handlers
    assert "/execution-plans" not in context_handlers
