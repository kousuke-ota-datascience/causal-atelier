"""Focused ENH-E5 G02 P03 navigation/read-surface regression checks."""

from __future__ import annotations

import subprocess
from pathlib import Path


REPOSITORY = Path(__file__).parents[2]


def test_all_predictive_stages_have_canonical_routes_without_execution_aliases() -> None:
    script = f"""
const fs = require('fs'); const vm = require('vm');
vm.runInThisContext(fs.readFileSync({str(REPOSITORY / 'frontend/navigation_state.js')!r}, 'utf8'));
const catalog = {{families:[{{slug:'predictive',default_stage_id:'setup',stages:[
  'setup','train','predict','metrics','explainability','model-management'
].map(slug=>({{slug}}))}}]}};
const n = globalThis.AnalysisNavigation;
for (const stage of catalog.families[0].stages) {{
  const route = n.serialize(n.navigationContext(catalog, 'p1', 'predictive', stage.slug));
  if (route !== `/projects/p1/analysis/predictive/${{stage.slug}}`) throw Error(route);
}}
"""
    result = subprocess.run(["node", "-e", script], capture_output=True, text=True, check=False)
    assert result.returncode == 0, result.stderr or result.stdout


def test_predictive_draft_is_route_independent_and_read_surfaces_do_not_create_execution() -> None:
    javascript = (REPOSITORY / "frontend" / "app.js").read_text(encoding="utf-8")
    html = (REPOSITORY / "frontend" / "index.html").read_text(encoding="utf-8")
    assert "predictiveDraft:null" in javascript
    assert "function capturePredictiveDraft()" in javascript
    assert "function restorePredictiveDraft()" in javascript
    assert "restorePredictiveDraft();" in javascript

    details = javascript.split("function renderPredictiveDetails()", 1)[1].split(
        "window.showPredictiveExecution", 1
    )[0]
    assert "/executions" not in details
    assert "state.predictiveDetails" in details
    assert "PREDICTIVE_EXPLANATION_RESULT" in javascript
    assert "Predictive Explanation ≠ Causal Explanation ≠ Treatment Effect" in html
    assert "ModelRegistry" not in javascript


def test_no_new_model_registry_or_navigation_persistence_is_introduced() -> None:
    source = (REPOSITORY / "src/ariadne/product/application/navigation_catalog.py").read_text(encoding="utf-8")
    repository_source = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (REPOSITORY / "src" / "ariadne").rglob("*.py")
    )
    assert "ModelRegistry" not in repository_source
    assert "ExecutionPlan" not in source
    assert "StageExecution" not in source
