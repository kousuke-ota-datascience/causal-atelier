"""Focused ENH-E5 G03 P01 causal navigation presentation checks."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


REPOSITORY = Path(__file__).parents[2]
PRESENTATION = REPOSITORY / "frontend" / "causal_stage_presentation.js"


def _stage_presentation() -> dict[str, dict[str, object]]:
    script = f"""
const fs = require('fs');
const vm = require('vm');
vm.runInThisContext(fs.readFileSync({str(PRESENTATION)!r}, 'utf8'));
console.log(JSON.stringify(globalThis.CausalStagePresentation.STAGES));
"""
    result = subprocess.run(["node", "-e", script], check=True, text=True, capture_output=True)
    return json.loads(result.stdout)


def test_causal_navigation_has_the_exact_seven_presentation_stages() -> None:
    stages = _stage_presentation()

    assert list(stages) == [
        "setup", "discovery", "identification", "estimation", "effects", "diagnostics", "sensitivity",
    ]
    assert all(stage["title"].lower() == stage_id for stage_id, stage in stages.items())


def test_read_stages_describe_saved_results_without_runtime_stage_mapping() -> None:
    source = PRESENTATION.read_text(encoding="utf-8")
    stages = _stage_presentation()

    assert "saved" in str(stages["effects"]["summary"]).lower()
    assert "saved" in str(stages["diagnostics"]["summary"]).lower()
    assert "saved" in str(stages["sensitivity"]["summary"]).lower()
    assert "ExecutionOperation" not in source
    assert "StageType" not in source
    assert "fetch(" not in source


def test_navigation_shell_renders_causal_presentation_only_for_causal_routes() -> None:
    html = (REPOSITORY / "frontend" / "index.html").read_text(encoding="utf-8")
    app = (REPOSITORY / "frontend" / "app.js").read_text(encoding="utf-8")

    assert '<script src="/causal_stage_presentation.js"></script>' in html
    assert 'id="causal-stage-presentation"' in html
    assert "context.familySlug!=='causal'" in app
    assert "CausalStagePresentation.presentationFor(context.stageSlug)" in app
