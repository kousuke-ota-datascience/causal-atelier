"""Factory functions for the discovery application service and requests."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from ariadne.application.discovery.adapters.artifact_writer import (
    LocalDiscoveryArtifactWriter,
)
from ariadne.application.discovery.adapters.backend import CausalLearnDiscoveryBackend
from ariadne.application.discovery.dto import (
    DiscoveryInputSpecification,
    DiscoveryRequest,
)
from ariadne.application.discovery.providers.completejourney import (
    CompleteJourneyDiscoveryInputProvider,
)
from ariadne.application.discovery.providers.registry import (
    DiscoveryInputProviderRegistry,
)
from ariadne.application.discovery.providers.single_table import (
    SingleTableDiscoveryInputProvider,
)
from ariadne.application.discovery.service import DiscoveryApplicationService
from ariadne.causal.discovery.config import (
    load_analysis_config,
    merge_cli_overrides,
    resolve_project_path,
)
from ariadne.causal.discovery.constants import (
    ALLOWED_ALGORITHMS,
    DEFAULT_ANALYSIS_CONFIG,
    DEFAULT_FEATURE_CONFIG,
    DEFAULT_PC_INDEP_TESTS,
)
from ariadne.preprocessing.discovery.config import load_feature_config

# ---------------------------------------------------------------------------
# Composition root
# ---------------------------------------------------------------------------


def build_discovery_application_service(
    project_root: Path | None = None,
) -> DiscoveryApplicationService:
    """Build the default DiscoveryApplicationService.

    Registers the ``completejourney`` and ``single_table`` providers.
    Additional providers can be registered on the returned registry after
    construction by accessing ``service._registry`` — or by replacing this
    factory in tests.

    Args:
        project_root: Repository root used for path resolution.  Ignored
            by the service itself but kept for symmetry with CLI usage.

    Returns:
        Configured DiscoveryApplicationService.
    """
    registry = _build_default_provider_registry()
    backend = CausalLearnDiscoveryBackend()
    writer = LocalDiscoveryArtifactWriter()
    return DiscoveryApplicationService(
        provider_registry=registry,
        backend=backend,
        artifact_writer=writer,
    )


def _build_default_provider_registry() -> DiscoveryInputProviderRegistry:
    """Return a registry pre-loaded with the built-in providers."""
    registry = DiscoveryInputProviderRegistry()
    registry.register(
        "completejourney",
        lambda request: CompleteJourneyDiscoveryInputProvider(request),
    )
    registry.register(
        "single_table",
        lambda request: SingleTableDiscoveryInputProvider(request),
    )
    return registry


# ---------------------------------------------------------------------------
# DiscoveryRequest construction (shared by CLI and Stage Runner)
# ---------------------------------------------------------------------------


def build_discovery_request(
    args: argparse.Namespace,
    project_root: Path,
) -> DiscoveryRequest:
    """Build an immutable DiscoveryRequest from parsed CLI arguments.

    This function is the single source of truth for converting a parsed
    argument namespace into the application-layer request.  Both the CLI
    thin adapter and the PipelineStageRunner call this function.

    Config resolution priority (highest first):
    1. Explicit CLI override
    2. provider / input config
    3. Legacy compatibility mapping (dataset.yaml_path, run.campaign_id, run.pre_weeks)
    4. Default

    Args:
        args: Parsed argument namespace produced by any compatible parser.
        project_root: Resolved repository root.

    Returns:
        Validated, immutable DiscoveryRequest.
    """
    if getattr(args, "dataset_yaml", None) is not None:
        args.dataset_yaml = args.dataset_yaml.resolve()
    if getattr(args, "output_dir", None) is not None:
        args.output_dir = args.output_dir.resolve()

    analysis_config_path = _resolve_config_path(
        getattr(args, "analysis_config", DEFAULT_ANALYSIS_CONFIG),
        project_root,
    )
    feature_config_path_raw = getattr(args, "feature_config", DEFAULT_FEATURE_CONFIG)
    feature_config_path: Path | None = _resolve_config_path(
        feature_config_path_raw, project_root
    )

    analysis_config = load_analysis_config(analysis_config_path)
    analysis_config = merge_cli_overrides(analysis_config, args)

    output_dir = resolve_project_path(analysis_config.run.output_dir, project_root)

    provider_type = getattr(args, "input_provider", None) or "completejourney"

    if provider_type == "completejourney":
        feature_config = (
            load_feature_config(feature_config_path)
            if feature_config_path is not None and feature_config_path.exists()
            else None
        )
        provider_options: dict[str, Any] = {}
    elif provider_type == "single_table":
        feature_config = None
        feature_config_path = None
        provider_options = dict(getattr(args, "provider_options", {}) or {})
    else:
        feature_config = None
        feature_config_path = None
        provider_options = {}

    return DiscoveryRequest(
        project_root=project_root,
        analysis_config_path=analysis_config_path,
        feature_config_path=feature_config_path,
        input_specification=DiscoveryInputSpecification(
            provider_type=provider_type,
            options=provider_options,
        ),
        analysis_config=analysis_config,
        feature_config=feature_config,
        output_dir=output_dir,
    )


def build_discovery_request_from_argv(
    argv: list[str] | None,
    project_root: Path | None = None,
) -> DiscoveryRequest:
    """Parse argv and build a DiscoveryRequest.

    Used by PipelineStageRunner so it does not import from interfaces.cli.
    The ``--project-root`` value from argv is used when ``project_root`` is None.

    Args:
        argv: Argument list (e.g. ``stage_plan.resolved_args``).
        project_root: Override for project root.  When None, the value from
            ``--project-root`` in argv is used.  If neither is available a
            ValueError is raised — callers are responsible for root detection.

    Returns:
        Validated DiscoveryRequest.

    Raises:
        ValueError: If project_root cannot be determined.
    """
    args, _ = _make_minimal_arg_parser().parse_known_args(argv)

    if project_root is None:
        if args.project_root is not None:
            project_root = Path(args.project_root).resolve()
        else:
            raise ValueError(
                "project_root could not be determined from argv. "
                "Pass --project-root in the argument list or supply project_root explicitly."
            )

    return build_discovery_request(args, project_root)


def _make_minimal_arg_parser() -> argparse.ArgumentParser:
    """Return a minimal parser for building DiscoveryRequest from argv lists.

    Unlike the CLI parser, this parser has no help text and does not exit
    on unknown arguments (callers use parse_known_args).
    """
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--project-root", type=Path, default=None)
    parser.add_argument("--analysis-config", type=Path, default=DEFAULT_ANALYSIS_CONFIG)
    parser.add_argument("--feature-config", type=Path, default=DEFAULT_FEATURE_CONFIG)
    parser.add_argument("--dataset-yaml", type=Path, default=None)
    parser.add_argument("--campaign-id", default=None)
    parser.add_argument("--pre-weeks", type=int, default=None)
    parser.add_argument("--alpha", type=float, default=None)
    parser.add_argument(
        "--pc-indep-test",
        choices=DEFAULT_PC_INDEP_TESTS,
        default=None,
    )
    parser.add_argument("--alpha-grid", nargs="+", type=float, default=None)
    parser.add_argument("--bootstrap-samples", type=int, default=None)
    parser.add_argument("--bootstrap-sample-fraction", type=float, default=None)
    parser.add_argument("--random-seed", type=int, default=None)
    parser.add_argument("--pc-discrete-bins", type=int, default=None)
    parser.add_argument("--collinearity-threshold", type=float, default=None)
    parser.add_argument(
        "--no-background-knowledge",
        action="store_true",
        default=None,
    )
    parser.add_argument("--output-dir", type=Path, default=None)
    parser.add_argument(
        "--algorithms",
        nargs="+",
        default=None,
        choices=ALLOWED_ALGORITHMS,
    )
    parser.add_argument("--notears-threshold", type=float, default=None)
    parser.add_argument("--input-provider", default=None)
    return parser


def _resolve_config_path(path: Path, project_root: Path) -> Path:
    """Resolve a config file path relative to project root."""
    if path.is_absolute():
        return path
    candidate = project_root / path
    if candidate.exists():
        return candidate
    return path.resolve()


__all__ = [
    "build_discovery_application_service",
    "build_discovery_request",
    "build_discovery_request_from_argv",
]
