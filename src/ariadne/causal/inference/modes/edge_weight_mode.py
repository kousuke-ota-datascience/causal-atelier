"""探索済み edge の重みを推定する analysis mode。"""

from __future__ import annotations

from ..context import RunContext
from ..estimators.edge_weight import EdgeWeightEstimator
from ..multiplicity import adjust_p_values
from ..reporting.markdown import render_edge_weight_report
from ..reporting.outputs import OutputWriter
from .base import AnalysisModeStrategy


class EdgeWeightModeStrategy(AnalysisModeStrategy):
    """edge weight estimation mode を実行する strategy。"""

    mode = "edge_weight"

    def run(self, context: RunContext) -> None:
        """edge weight 推定を実行し、結果を書き出す。

        Args:
            context: Resolved run context.

        Raises:
            FileNotFoundError: If required causal discovery edge files are
                missing.
            ValueError: If the analysis frame or edge schema is invalid.
        """
        config = context.config
        edge_config = config.edge_weight
        edge_weight = EdgeWeightEstimator(
            standardized_frame=context.standardized_frame,
            original_frame=context.inference_frame,
            discovery_dir=context.discovery_dir,
            output_dir=context.output_dir,
            algorithms=edge_config.algorithms,
            dropped_columns=context.preprocessing_result.dropped_columns,
            robust_se=edge_config.robust_se,
            min_samples=edge_config.min_samples,
        )
        effects, skipped_edges = edge_weight.estimate_all_edge_coefficients()
        if not effects.empty and "p_value" in effects:
            effects["p_value_adjusted"] = adjust_p_values(effects["p_value"], "bh_fdr")
            effects["adjustment_method"] = "bh_fdr"
            effects["interpretation_level"] = "exploratory_edge_coefficient"
            effects["diagnostic_status"] = "review_required"

        writer = OutputWriter(
            context.output_dir,
            write_csv=config.report.write_csv,
            write_markdown=config.report.write_markdown,
        )
        writer.write_csv_table("edge_weight/edge_effects.csv", effects)
        writer.write_csv_table("edge_weight/skipped_edges.csv", skipped_edges)
        writer.write_csv_table(
            "edge_weight/dropped_columns.csv",
            context.preprocessing_result.dropped_columns,
        )
        writer.write_csv_table("edge_effects.csv", effects)
        report = render_edge_weight_report(
            effects,
            skipped_edges,
            context.preprocessing_result.dropped_columns,
            config,
        )
        writer.write_markdown_text("edge_weight/edge_effects.md", report)
        writer.write_markdown_text("edge_effects.md", report)

        print(f"mode: {config.mode}")
        print(f"samples: {len(context.standardized_frame):,}")
        print(f"standardized_variables: {len(context.standardized_frame.columns):,}")
        print(f"discovery_dir: {context.discovery_dir}")
        print(f"output_dir: {context.output_dir}")
        print(effects.to_string(index=False))
