"""Focused ENH-E7 G03 P06 structural integration coverage."""
from pathlib import Path
REPOSITORY=Path(__file__).parents[2]
def test_surface_architecture_has_exclusive_roots_and_browser_evidence_for_each_surface():
    html=(REPOSITORY/'frontend/index.html').read_text(encoding='utf-8')
    authority=(REPOSITORY/'frontend/top_level_surface_activation.js').read_text(encoding='utf-8')
    browser=(REPOSITORY/'tests/browser_e2e/run_enh_e7_project_integration.py').read_text(encoding='utf-8')
    assert html.count('data-top-level-surface-root=')==3
    assert "root.hidden=!active" in authority
    for name in ('projects','project-management','analysis'):
        assert f'enh-e7-g03-p06-{name}.png' in browser
    assert '<aside' not in html
    assert 'data-hidden-on-projects-surface' not in authority
