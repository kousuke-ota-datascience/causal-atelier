"""Non-browser contract for the G05 browser-owned critical causal journey."""

import ast
from pathlib import Path


def _repository_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").is_file():
            return parent
    raise RuntimeError("repository root not found")


RUNNER = _repository_root() / "tests/enhancement/enh_e9/g05/browser_e2e/run_critical_causal_journey.py"
ROOT = _repository_root()


def test_critical_journey_runner_is_current_ui_and_syntax_valid() -> None:
    source = RUNNER.read_text(encoding="utf-8")
    ast.parse(source)

    for required in (
        "#project-register-form", "#dataset-form", "#discovery-form", "#graph-candidates",
        "#run-identification", "#identification-results", "#run-estimation",
        "#treatment-effect-results", "#diagnostics-results",
    ):
        assert required in source
    assert "run_enh_e1a" not in source


def test_critical_journey_tracks_one_project_context_dataset_graph_and_result_lineage() -> None:
    source = RUNNER.read_text(encoding="utf-8")

    for lineage_key in (
        '"project_id"', '"dataset_version_id"', '"graph_version_id"',
        '"identification_execution_id"', '"identification_result_id"',
        '"estimation_execution_id"', '"treatment_effect_result_id"', '"diagnostics_result_id"',
    ):
        assert lineage_key in source
    assert 'page.locator("#identification-results").select_option(identification_result["result_id"])' in source
    assert 'next(item for item in results if item["result_type"] == "TREATMENT_EFFECT_RESULT")' in source
    assert 'next(item for item in results if item["result_type"] == "DIAGNOSTICS_RESULT")' in source


def test_critical_journey_uses_observable_readiness_and_retains_failure_evidence() -> None:
    source = RUNNER.read_text(encoding="utf-8")

    assert "def _wait(" in source
    assert "page.wait_for_function" in source
    assert "dataset.refreshStatus === 'done'" in source
    assert "time.sleep(0.5)" in source  # retry pacing is inside observable _wait, never authority alone.
    assert '"route": page.url' in source
    assert '"last_checkpoint"' in source
    assert "page.screenshot(path=FAILURE" in source
    assert "context.tracing.start" in source
    assert 'page.on("console"' in source


def test_browser_image_build_context_includes_the_g05_runner() -> None:
    dockerfile = (ROOT / "Dockerfile.browser-e2e").read_text(encoding="utf-8")
    dockerignore = (ROOT / ".dockerignore").read_text(encoding="utf-8")

    runner = "tests/enhancement/enh_e9/g05/browser_e2e/run_critical_causal_journey.py"
    assert runner in dockerfile
    assert "!tests/enhancement/enh_e9/g05/" in dockerignore
    assert "!tests/enhancement/enh_e9/g05/browser_e2e/" in dockerignore
    assert f"!{runner}" in dockerignore
