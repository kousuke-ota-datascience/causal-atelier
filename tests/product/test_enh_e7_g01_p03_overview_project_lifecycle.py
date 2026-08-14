"""Focused ENH-E7 G01 P03 coverage for Overview Project lifecycle ownership."""

import re
from pathlib import Path


REPOSITORY = Path(__file__).parents[2]


def _section(html: str, section_id: str) -> str:
    match = re.search(
        rf'<section id="{section_id}" class="workspace.*?</section>', html, flags=re.DOTALL
    )
    assert match is not None
    return match.group(0)


def test_overview_owns_selected_project_identity_metadata_status_and_archive() -> None:
    html = (REPOSITORY / "frontend" / "index.html").read_text(encoding="utf-8")
    app = (REPOSITORY / "frontend" / "app.js").read_text(encoding="utf-8")
    overview = _section(html, "management")

    assert 'id="project-form"' in overview
    assert 'id="overview-project-name"' in overview
    assert 'id="overview-project-status"' in overview
    assert 'id="archive-project"' in overview
    assert "$('#overview-project-status').textContent=state.project?.status||'—';" in app
    assert "$('#archive-project').onclick=()=>{if(state.project)requestArchive(state.project.project_id)};" in app


def test_selected_project_defaults_to_overview_and_data_does_not_own_metadata() -> None:
    html = (REPOSITORY / "frontend" / "index.html").read_text(encoding="utf-8")
    app = (REPOSITORY / "frontend" / "app.js").read_text(encoding="utf-8")
    data = _section(html, "data")

    assert "PROJECT_WORKSPACES=Object.freeze({overview:'management'" in app
    assert "ProjectNavigation.overview(state.project.project_id)" in app
    assert 'id="project-form"' not in data
    assert 'id="dataset-form"' in data
    assert 'id="analysis-view-form"' not in _section(html, "management")
