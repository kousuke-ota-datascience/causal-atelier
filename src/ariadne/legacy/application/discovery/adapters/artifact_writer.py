"""Local filesystem artifact writer for causal discovery."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ariadne.application.discovery.dto import (
    DiscoveryArtifactResult,
    DiscoveryRequest,
    PreparedDiscoveryInput,
)
from ariadne.causal.discovery.algorithms import CausalDiscovery
from ariadne.causal.discovery.config import write_resolved_config
from ariadne.causal.discovery.diagnostics import CausalDiscoveryDiagnostics
from ariadne.causal.discovery.reporting import CausalDiscoveryReporter


class LocalDiscoveryArtifactWriter:
    """Writes discovery outputs to the local filesystem.

    Reuses CausalDiscoveryReporter for all CSV/Markdown outputs and
    write_resolved_config for reproducibility snapshots.  Does not perform
    any causal discovery computation.
    """

    def write(
        self,
        request: DiscoveryRequest,
        prepared_input: PreparedDiscoveryInput,
        algorithm_results: dict[str, Any],
    ) -> DiscoveryArtifactResult:
        """Write all configured discovery outputs.

        Args:
            request: Original discovery request (provides config paths and output dir).
            prepared_input: Frames and metadata for reporting.
            algorithm_results: Per-algorithm DiscoveryResult from the backend.

        Returns:
            Written artifact paths.
        """
        output_dir = request.output_dir
        analysis_config = request.analysis_config

        if request.feature_config is not None:
            write_resolved_config(
                analysis_config=analysis_config,
                feature_config=request.feature_config,
                output_dir=output_dir,
            )

        # Build a CausalDiscovery instance solely for the diagnostics helper.
        # No algorithms are run here.
        disc_cfg = analysis_config.discovery
        diag_cfg = analysis_config.diagnostics
        discovery_runner = CausalDiscovery(
            alpha=disc_cfg.pc.alpha,
            use_background_knowledge=False,
            feature_config=request.feature_config,
            algorithms=disc_cfg.algorithms,
            notears_threshold=disc_cfg.notears.threshold,
            pc_indep_test=disc_cfg.pc.indep_test,
            allowed_pc_indep_tests=disc_cfg.pc.allowed_indep_tests,
            discrete_pc_indep_tests=disc_cfg.pc.discrete_indep_tests,
            alpha_grid=disc_cfg.pc.alpha_grid,
            bootstrap_samples=diag_cfg.bootstrap.samples,
            bootstrap_sample_fraction=diag_cfg.bootstrap.sample_fraction,
            random_seed=analysis_config.run.random_seed,
            pc_discrete_bins=disc_cfg.pc.discrete_bins,
            ges_max_p=disc_cfg.ges.maxP,
            ges_score_func=disc_cfg.ges.score_func,
        )

        reporter = CausalDiscoveryReporter(
            reporting_config=analysis_config.reporting,
            diagnostics=CausalDiscoveryDiagnostics(discovery_runner),
        )

        retained_columns = list(prepared_input.analysis_frame.columns)
        raw_frame = (
            prepared_input.raw_frame.loc[:, retained_columns]
            if prepared_input.raw_frame is not None
            else prepared_input.analysis_frame
        )
        transformed_frame = (
            prepared_input.transformed_frame.loc[:, retained_columns]
            if prepared_input.transformed_frame is not None
            else prepared_input.analysis_frame
        )

        # Extract Complete Journey–style metadata for reporter display strings.
        campaign_id = str(prepared_input.metadata.get("campaign_id", ""))
        pre_weeks_raw = prepared_input.metadata.get("pre_weeks", 0)
        pre_weeks = int(pre_weeks_raw) if pre_weeks_raw is not None else 0
        collinearity_threshold = float(
            prepared_input.metadata.get(
                "collinearity_threshold",
                analysis_config.preprocessing.collinearity_threshold,
            )
        )

        reporter.write_outputs(
            results=algorithm_results,
            raw_discovery_frame=raw_frame,
            discovery_frame=transformed_frame,
            standardized_frame=prepared_input.analysis_frame,
            variable_metadata=prepared_input.variable_metadata,
            output_dir=output_dir,
            collinearity_threshold=collinearity_threshold,
            campaign_id=campaign_id,
            pre_weeks=pre_weeks,
        )

        artifacts = self._collect_artifacts(output_dir, algorithm_results)
        return DiscoveryArtifactResult(artifacts=artifacts)

    @staticmethod
    def _collect_artifacts(
        output_dir: Path,
        algorithm_results: dict[str, Any],
    ) -> dict[str, Path]:
        """Collect existing artifact paths by well-known names."""
        planned: dict[str, Path] = {
            "resolved_config": output_dir / "resolved_analysis_config.yaml",
            "resolved_feature_config": output_dir / "resolved_features_config.yaml",
        }
        for algorithm in algorithm_results:
            algo_dir = output_dir / algorithm
            planned[f"edges_{algorithm}"] = algo_dir / "edges.csv"
            if algorithm == "pc":
                planned["bootstrap_summary"] = algo_dir / "edge_stability.csv"

        return {name: path for name, path in planned.items() if path.exists()}


__all__ = ["LocalDiscoveryArtifactWriter"]
