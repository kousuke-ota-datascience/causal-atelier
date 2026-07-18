"""明示的な treatment effect を推定する analysis mode。"""

from __future__ import annotations

import pandas as pd

from ..context import RunContext
from ..diagnostics.design import DesignDiagnostics
from ..diagnostics.overlap import summarize_propensity_overlap
from ..estimators.treatment_effect import (
    TreatmentEffectEstimator,
    validate_treatment_effect_inputs,
)
from ..multiplicity import adjust_p_values
from causal_atelier.preprocessing.inference.selectors import select_adjustment_set
from ..reporting.markdown import render_treatment_effect_report
from ..reporting.outputs import OutputWriter
from .base import AnalysisModeStrategy


class TreatmentEffectModeStrategy(AnalysisModeStrategy):
    """treatment effect estimation mode を実行する strategy。"""

    mode = "treatment_effect"

    def run(self, context: RunContext) -> None:
        """treatment effect 推定を実行し、結果を書き出す。

        Args:
            context: Resolved run context.

        Raises:
            ValueError: If treatment, outcome, or adjustment configuration is
                invalid.
        """
        config = context.config
        te_config = config.treatment_effect
        inference_frame = context.inference_frame
        validate_treatment_effect_inputs(
            inference_frame,
            te_config.treatment,
            te_config.outcome,
        )
        graph_edges = self.load_graph_edges_for_adjustment(context)
        adjustment_result = select_adjustment_set(
            inference_frame,
            feature_config=context.feature_config,
            treatment=te_config.treatment,
            outcome=te_config.outcome,
            strategy=te_config.adjustment_strategy,
            manual_covariates=te_config.covariates,
            graph_edges=graph_edges,
        )
        adjustment_set = adjustment_result.selected
        estimator = TreatmentEffectEstimator(
            inference_frame,
            treatment=te_config.treatment,
            outcome=te_config.outcome,
            covariates=adjustment_set,
            estimand=te_config.estimand,
            robust_se=te_config.robust_se,
            propensity_clip=te_config.propensity_clip,
            cross_fitting_folds=te_config.cross_fitting_folds,
        )
        effects = estimator.estimate(list(te_config.effect_methods))
        if not effects.empty:
            effects["p_value_adjusted"] = adjust_p_values(effects["p_value"], "bh_fdr")
            effects["adjustment_method"] = te_config.adjustment_strategy
            effects["n_units"] = effects["n"]
            effects["effective_sample_size"] = pd.NA
            effects["diagnostic_status"] = "review_required"
            effects["interpretation_level"] = effects["method"].map(
                lambda method: "regression_coefficient"
                if method == "ols_coefficient"
                else "identified_estimand_under_assumptions"
            )
            effects["warnings"] = effects["notes"].fillna("")
        diagnostics = DesignDiagnostics(
            frame=inference_frame,
            treatment=te_config.treatment,
            outcome=te_config.outcome,
            covariates=adjustment_set,
        )
        diagnostic_tables = {
            "design": diagnostics.treatment_counts(),
            "balance": diagnostics.balance_table(),
            "outcome_distribution": diagnostics.outcome_distribution(),
            "propensity_overlap": self.build_propensity_overlap(context, estimator),
        }

        writer = OutputWriter(
            context.output_dir,
            write_csv=config.report.write_csv,
            write_markdown=config.report.write_markdown,
        )
        writer.write_csv_table("treatment_effect/treatment_effects.csv", effects)
        writer.write_csv_table(
            "treatment_effect/design_diagnostics.csv",
            diagnostic_tables["design"],
        )
        writer.write_csv_table("treatment_effect/balance_table.csv", diagnostic_tables["balance"])
        writer.write_csv_table(
            "treatment_effect/propensity_overlap.csv",
            diagnostic_tables["propensity_overlap"],
        )
        writer.write_csv_table(
            "treatment_effect/outcome_distribution.csv",
            diagnostic_tables["outcome_distribution"],
        )
        writer.write_csv_table(
            "treatment_effect/selected_adjustment_set.csv",
            pd.DataFrame({"covariate": adjustment_set}),
        )
        writer.write_csv_table(
            "treatment_effect/excluded_adjustment_candidates.csv",
            adjustment_result.excluded,
        )
        report = render_treatment_effect_report(
            effects,
            diagnostic_tables,
            config,
            adjustment_set=adjustment_set,
        )
        writer.write_markdown_text("treatment_effect/treatment_effects.md", report)

        print(f"mode: {config.mode}")
        print(f"samples: {len(inference_frame):,}")
        print(f"variables: {len(inference_frame.columns):,}")
        print(f"adjustment_set: {', '.join(adjustment_set) if adjustment_set else '(none)'}")
        print(f"output_dir: {context.output_dir}")
        print(effects.to_string(index=False))

    def load_graph_edges_for_adjustment(self, context: RunContext) -> pd.DataFrame | None:
        """graph-parent adjustment が指定された場合だけ探索 edge を読み込む。

        Args:
            context: Resolved run context.

        Returns:
            Edge table or ``None`` when not needed.
        """
        if context.config.treatment_effect.adjustment_strategy != "graph_parents":
            return None
        from ..discovery_artifacts.edges import load_discovery_edges

        return load_discovery_edges(
            context.discovery_dir,
            context.config.edge_weight.algorithms,
            required=False,
        )

    def build_propensity_overlap(
        self,
        context: RunContext,
        estimator: TreatmentEffectEstimator,
    ) -> pd.DataFrame:
        """最後に推定した propensity score から overlap 出力を作る。

        Args:
            context: Resolved run context.
            estimator: Treatment-effect estimator after method execution.

        Returns:
            Propensity overlap table.
        """
        if estimator.last_propensity_score is None:
            return pd.DataFrame(
                columns=[
                    "ps_min",
                    "ps_p01",
                    "ps_p05",
                    "ps_median",
                    "ps_p95",
                    "ps_p99",
                    "ps_max",
                    "n_ps_below_0_01",
                    "n_ps_above_0_99",
                ]
            )
        return summarize_propensity_overlap(
            estimator.last_propensity_score,
            context.config.treatment_effect.propensity_clip,
        )
