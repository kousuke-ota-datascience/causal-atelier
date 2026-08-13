"""Static guardrails for the ENH-E6 real-browser runner integration."""

from pathlib import Path


REPOSITORY = Path(__file__).parents[2]


def test_e6_runner_is_in_docker_context_and_covers_actual_navigation_controls() -> None:
    runner = (REPOSITORY / "tests/browser_e2e/run_enh_e6_family_stage_navigation.py").read_text(encoding="utf-8")
    dockerfile = (REPOSITORY / "Dockerfile.browser-e2e").read_text(encoding="utf-8")
    ignored = (REPOSITORY / ".dockerignore").read_text(encoding="utf-8")

    assert "run_enh_e6_family_stage_navigation.py" in dockerfile
    assert "!tests/browser_e2e/run_enh_e6_family_stage_navigation.py" in ignored
    assert "#analysis-family-tabs" in runner
    assert "#analysis-stage-sidebar" in runner
    assert "B01-normal-entry-family-switching" in runner
    assert "B02-causal-discovery-inference-boundary" in runner
    assert "B03-direct-reload-history-restore" in runner
    assert "page.reload" in runner and "page.go_back" in runner and "page.go_forward" in runner
