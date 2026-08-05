"""CLI execution management tests.

Verifies the normative policy from v1.4 requirements:
  - CLI runs do NOT create Ariadne Executions.
  - PipelinePlanner does NOT generate pseudo Ariadne execution_ids.
  - run_label is None when --run-label is not provided.
  - --run-id (deprecated) acts as alias for --run-label.
  - --run-label is used as the manifest label.
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock

import pytest

from ariadne.application.pipeline.planning import ExecutionPlan, PipelinePlanner
from ariadne.interfaces.cli.pipeline import parse_args


class TestPlannerNoUUIDGeneration:
    def test_run_label_is_none_when_not_provided(self) -> None:
        args = parse_args(["--project-root", str(Path.cwd())])
        plan = PipelinePlanner(Path.cwd()).build_plan(args, strategy_name="dry_run")
        assert plan.run_label is None

    def test_run_label_from_run_label_option(self) -> None:
        args = parse_args(["--run-label", "my-experiment"])
        plan = PipelinePlanner(Path.cwd()).build_plan(args, strategy_name="dry_run")
        assert plan.run_label == "my-experiment"

    def test_run_label_from_deprecated_run_id(self) -> None:
        args = parse_args(["--run-id", "legacy-label"])
        plan = PipelinePlanner(Path.cwd()).build_plan(args, strategy_name="dry_run")
        assert plan.run_label == "legacy-label"

    def test_run_label_is_not_a_uuid_hex(self) -> None:
        """Planner must not silently generate a UUID when no label is given."""
        args = parse_args(["--project-root", str(Path.cwd())])
        plan = PipelinePlanner(Path.cwd()).build_plan(args, strategy_name="dry_run")
        assert plan.run_label is None, (
            "PipelinePlanner must not generate a pseudo UUID for CLI runs. "
            "Got: " + repr(plan.run_label)
        )


class TestCLINoAriadneExecutionCreated:
    def test_execution_plan_has_no_ariadne_execution_id_field(self) -> None:
        """ExecutionPlan must not expose an 'execution_id' attribute."""
        assert not hasattr(ExecutionPlan, "execution_id"), (
            "ExecutionPlan must not have execution_id field; CLI does not create Ariadne Executions. "
            "Use run_label for human-readable manifest labels."
        )

    def test_execution_plan_dry_run_output_has_run_label_not_execution_id(self) -> None:
        args = parse_args(["--run-label", "test-label"])
        plan = PipelinePlanner(Path.cwd()).build_plan(args, strategy_name="dry_run")
        serialized = plan.to_dict()
        assert "run_label" in serialized
        assert "execution_id" not in serialized

    def test_no_execution_id_option_in_cli_parser(self) -> None:
        """--execution-id must not be a supported option (removed in v1.4)."""
        with pytest.raises(SystemExit):
            parse_args(["--execution-id", "should-fail"])


class TestCLINoMetadataDBConnection:
    def test_dry_run_does_not_require_database(self) -> None:
        """CLI dry-run must not attempt a DB connection."""
        from ariadne.application.pipeline.strategies import DryRunStrategy

        args = parse_args(["--run-label", "no-db-test"])
        plan = PipelinePlanner(Path.cwd()).build_plan(args, strategy_name="dry_run")
        result = DryRunStrategy().execute(plan)
        assert result.status == "ok"
        assert result.payload is not None
        assert result.payload["run_label"] == "no-db-test"
