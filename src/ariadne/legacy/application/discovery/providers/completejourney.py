"""CompleteJourney input provider for causal discovery."""

from __future__ import annotations

from ariadne.application.discovery.dto import (
    DiscoveryRequest,
    PreparedDiscoveryInput,
)
from ariadne.causal.discovery.config import resolve_project_path
from ariadne.etl.registry import LogicalTableDataLoader
from ariadne.preprocessing.discovery.builder import CompleteJourneyPreprocessor


class CompleteJourneyDiscoveryInputProvider:
    """Prepares Complete Journey input for causal discovery.

    Loads raw tables via LogicalTableDataLoader, runs CompleteJourneyPreprocessor,
    and returns a normalised PreparedDiscoveryInput.  This class is the only
    component that knows about campaign IDs, pre-treatment weeks, or Complete
    Journey table names.

    Args:
        request: Discovery request providing project_root, analysis_config,
            and feature_config.
    """

    def __init__(self, request: DiscoveryRequest) -> None:
        self._request = request

    def prepare(self, request: DiscoveryRequest) -> PreparedDiscoveryInput:
        """Load Complete Journey tables, preprocess, and normalise.

        Args:
            request: Discovery request with project_root, analysis_config,
                and feature_config.

        Returns:
            Normalised discovery input.

        Raises:
            ValueError: If feature_config is None.
        """
        if request.feature_config is None:
            raise ValueError(
                "CompleteJourneyDiscoveryInputProvider requires a feature_config"
            )

        analysis_config = request.analysis_config
        feature_config = request.feature_config
        project_root = request.project_root

        dataset_yaml = resolve_project_path(
            analysis_config.dataset.yaml_path, project_root
        )
        data_loader = LogicalTableDataLoader(
            project_root=project_root,
            dataset_yaml=dataset_yaml,
            table_specs=feature_config.tables,
            logger_name="causal_discovery",
        )
        tables = data_loader.load_all()

        preprocessor = CompleteJourneyPreprocessor(
            tables=tables,
            campaign_id=analysis_config.run.campaign_id,
            pre_weeks=analysis_config.run.pre_weeks,
            collinearity_threshold=analysis_config.preprocessing.collinearity_threshold,
            feature_config=feature_config,
        )
        result = preprocessor.preprocess()

        # Build background knowledge via CausalDiscovery helper to keep numerical
        # behaviour unchanged while decoupling it from the backend.
        background_knowledge = self._build_background_knowledge(
            result.standardized.columns.tolist(),
            analysis_config,
            feature_config,
        )

        return PreparedDiscoveryInput(
            analysis_frame=result.standardized,
            raw_frame=result.raw_discovery_frame,
            transformed_frame=result.discovery_frame,
            variable_metadata=result.variable_metadata,
            background_knowledge=background_knowledge,
            metadata={
                "campaign_id": analysis_config.run.campaign_id,
                "pre_weeks": analysis_config.run.pre_weeks,
                "collinearity_threshold": analysis_config.preprocessing.collinearity_threshold,
            },
        )

    @staticmethod
    def _build_background_knowledge(
        node_names: list[str],
        analysis_config,
        feature_config,
    ) -> object | None:
        """Build causal-learn BackgroundKnowledge from feature tiers.

        Returns None when background knowledge is disabled.
        """
        if not analysis_config.discovery.use_background_knowledge:
            return None

        from ariadne.causal.discovery.algorithms import CausalDiscovery

        # Temporary instance used only to build background knowledge; no
        # discovery is run here.
        helper = CausalDiscovery(
            alpha=analysis_config.discovery.pc.alpha,
            use_background_knowledge=True,
            feature_config=feature_config,
        )
        return helper.build_background_knowledge(node_names)


__all__ = ["CompleteJourneyDiscoveryInputProvider"]
