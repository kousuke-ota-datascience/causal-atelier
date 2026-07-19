"""End-to-end discovery and inference application service."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .planning import PipelinePlanner
from .strategies import PipelineCommandResult, select_strategy


def execute(args: Any, project_root: Path) -> PipelineCommandResult:
    """Build and execute the pipeline strategy selected by CLI arguments."""

    strategy = select_strategy(
        dry_run=bool(args.dry_run),
        validate_only=bool(args.validate_only),
    )
    plan = PipelinePlanner(project_root).build_plan(args, strategy_name=strategy.name)
    return strategy.execute(plan)


__all__ = ["execute"]
