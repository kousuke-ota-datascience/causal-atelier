"""Focused ENH-E6 G01 P02 presentation and legacy shortcut coverage."""

from __future__ import annotations

import subprocess
from pathlib import Path


REPOSITORY = Path(__file__).parents[2]


def test_presentation_resolver_maps_all_supported_surfaces_and_fails_closed() -> None:
    resolver = REPOSITORY / "frontend" / "analysis_presentation.js"
    script = f"""
const fs = require('fs'); const vm = require('vm');
vm.runInThisContext(fs.readFileSync({str(resolver)!r}, 'utf8'));
const resolve = globalThis.AnalysisPresentation.resolve;
const expected = {{
  'exploratory/profile':'explore', 'predictive/setup':'predictive',
  'causal/setup':'discovery', 'causal/discovery':'discovery',
  'causal/identification':'inference', 'causal/estimation':'inference',
  'causal/effects':'inference', 'causal/diagnostics':'inference', 'causal/sensitivity':'inference',
}};
for (const [key, workspace] of Object.entries(expected)) {{
  const [familySlug, stageSlug] = key.split('/');
  if (resolve({{familySlug, stageSlug}}).workspace !== workspace) throw Error(key);
}}
try {{ resolve({{familySlug:'causal',stageSlug:'unsupported'}}); throw Error('missing binding accepted'); }}
catch (error) {{ if (!String(error.message).includes('Missing analysis presentation binding')) throw error; }}
"""
    result = subprocess.run(["node", "-e", script], text=True, capture_output=True, check=False)
    assert result.returncode == 0, result.stderr or result.stdout


def test_legacy_shortcuts_submit_exact_canonical_contexts_to_p01_seam() -> None:
    html = (REPOSITORY / "frontend" / "index.html").read_text(encoding="utf-8")
    app = (REPOSITORY / "frontend" / "app.js").read_text(encoding="utf-8")

    for family, stage in (("exploratory", "profile"), ("predictive", "setup"), ("causal", "discovery"), ("causal", "identification")):
        assert f'data-navigation-family="{family}" data-navigation-stage="{stage}"' in html
    assert "source:'legacy-analytical-shortcut'" in app
    assert "AnalysisNavigation.navigationContext(state.navigationCatalog,state.project.project_id,shortcutFamily,shortcutStage)" in app
    assert "return applyAnalysisNavigation(context,{historyMode:ANALYSIS_HISTORY_MODES.PUSH" in app


def test_shared_transition_uses_stage_aware_presentation_not_family_only_causal_mapping() -> None:
    app = (REPOSITORY / "frontend" / "app.js").read_text(encoding="utf-8")

    assert "const presentation=AnalysisPresentation.resolve(next);" in app
    assert "await activateWorkspace(presentation.workspace,{push:false});" in app
    assert "ANALYSIS_WORKSPACES" not in app
