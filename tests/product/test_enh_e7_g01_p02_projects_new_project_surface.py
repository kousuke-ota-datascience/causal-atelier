"""Focused ENH-E7 G01 P02 coverage for Project List and New Project surfaces."""

from pathlib import Path


REPOSITORY = Path(__file__).parents[2]


def test_project_list_and_register_are_separate_route_backed_surfaces() -> None:
    source = (REPOSITORY / "frontend" / "app.js").read_text(encoding="utf-8")
    html = (REPOSITORY / "frontend" / "index.html").read_text(encoding="utf-8")

    assert '<section id="projects" class="workspace">' in html
    assert '<section id="project-new" class="workspace">' in html
    assert '<form id="project-register-form"' in html
    assert 'id="cancel-project-register"' in html
    assert "route.kind==='collection'?'projects':'project-new'" in source
    assert "await activateWorkspace('project-new',{push:false})" in source
    assert "await activateWorkspace('projects',{push:false})" in source


def test_create_transitions_to_new_project_overview_and_cancel_returns_to_list() -> None:
    source = (REPOSITORY / "frontend" / "app.js").read_text(encoding="utf-8")

    assert "ProjectNavigation.overview(state.project.project_id),'REPLACE'" in source
    assert "synchronizeProjectHistory(ProjectNavigation.overview(state.project.project_id),'REPLACE');await activateWorkspace('management',{push:false});" in source
    assert "$('#cancel-project-register').onclick=async()=>{synchronizeProjectHistory({kind:'collection'},'PUSH');" in source


def test_archive_is_not_a_global_project_list_responsibility() -> None:
    source = (REPOSITORY / "frontend" / "app.js").read_text(encoding="utf-8")
    html = (REPOSITORY / "frontend" / "index.html").read_text(encoding="utf-8")

    assert "onclick=\"requestArchive(" not in source
    assert "id=\"archive-project\"" in html
    assert "$('#archive-project').onclick=()=>{if(state.project)requestArchive(state.project.project_id)};" in source
