"""CausalLearn backend adapter for DiscoveryBackend."""

from __future__ import annotations

from typing import Any

from ariadne.application.discovery.dto import PreparedDiscoveryInput
from ariadne.causal.discovery.algorithms import CausalDiscovery
from ariadne.causal.discovery.config import AnalysisConfig


class CausalLearnDiscoveryBackend:
    """Adapts CausalDiscovery to the DiscoveryBackend protocol.

    Receives a PreparedDiscoveryInput (which already contains pre-built
    background knowledge) and runs the configured algorithms.  Does not know
    about Complete Journey, CLI arguments, or output paths.
    """

    def discover(
        self,
        prepared_input: PreparedDiscoveryInput,
        analysis_config: AnalysisConfig,
    ) -> dict[str, Any]:
        """Run all configured algorithms on the prepared analysis frame.

        Args:
            prepared_input: Normalised input including the analysis frame and
                pre-built background knowledge.
            analysis_config: Algorithm and diagnostic configuration.

        Returns:
            Mapping from algorithm name to DiscoveryResult.
        """
        disc_cfg = analysis_config.discovery
        diag_cfg = analysis_config.diagnostics

        # feature_config=None because background knowledge is pre-built in
        # prepared_input; use_background_knowledge=False tells CausalDiscovery
        # not to attempt building it internally.
        runner = CausalDiscovery(
            alpha=disc_cfg.pc.alpha,
            use_background_knowledge=False,
            feature_config=None,
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

        # Inject pre-built background knowledge before running PC.
        # run_all is called with background_knowledge forwarded so the
        # algorithm uses the provider-built knowledge without rebuilding it.
        return runner.run_all(
            prepared_input.analysis_frame,
            background_knowledge=prepared_input.background_knowledge,
        )


__all__ = ["CausalLearnDiscoveryBackend"]
