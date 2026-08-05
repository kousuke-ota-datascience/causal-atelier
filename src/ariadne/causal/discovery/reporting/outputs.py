from __future__ import annotations

from pathlib import Path

import pandas as pd

from ..graph import dataframe_to_markdown, mermaid_edge

from ..config import ReportingConfig
from ..diagnostics import CausalDiscoveryDiagnostics, variable_diagnostics
from ..results import DiscoveryResult


class CausalDiscoveryReporter:
    """因果探索の CSV 出力と Markdown graph report を書き出す。

    Args:
        reporting_config: Output switches loaded from analysis configuration.
        diagnostics: Diagnostic runner used for PC sensitivity and stability
            outputs.
    """

    def __init__(
        self,
        *,
        reporting_config: ReportingConfig,
        diagnostics: CausalDiscoveryDiagnostics,
    ) -> None:
        """reporter を初期化する。

        Args:
            reporting_config: Output switches loaded from analysis configuration.
            diagnostics: Diagnostic runner used for PC sensitivity and stability
                outputs.
        """
        self.reporting_config = reporting_config
        self.diagnostics = diagnostics

    def write_outputs(
        self,
        *,
        results: dict[str, DiscoveryResult],
        raw_discovery_frame: pd.DataFrame,
        discovery_frame: pd.DataFrame,
        standardized_frame: pd.DataFrame,
        variable_metadata: pd.DataFrame,
        output_dir: Path,
        collinearity_threshold: float,
        campaign_id: str,
        pre_weeks: int,
    ) -> None:
        """設定された workflow 出力をすべて書き出す。

        Args:
            results: Discovery results keyed by algorithm name.
            raw_discovery_frame: Raw feature frame before configured transforms.
            discovery_frame: Transformed feature frame before standardization.
            standardized_frame: Standardized input used by algorithms.
            variable_metadata: Variable metadata table.
            output_dir: Root output directory.
            collinearity_threshold: Threshold used during preprocessing.
            campaign_id: Campaign identifier analyzed.
            pre_weeks: Number of pre-treatment weeks.
        """
        output_dir.mkdir(parents=True, exist_ok=True)
        if self.reporting_config.write_raw_input:
            raw_discovery_frame.to_csv(
                output_dir / "causal_discovery_input_raw.csv",
                index=False,
            )
        if self.reporting_config.write_processed_input:
            discovery_frame.to_csv(output_dir / "causal_discovery_input.csv", index=False)
        if self.reporting_config.write_standardized_input:
            standardized_frame.to_csv(
                output_dir / "causal_discovery_input_standardized.csv",
                index=False,
            )
        if self.reporting_config.write_variable_metadata:
            variable_metadata.to_csv(output_dir / "variable_metadata.csv", index=False)
        if self.reporting_config.write_variable_diagnostics:
            variable_diagnostics(discovery_frame, variable_metadata).to_csv(
                output_dir / "variable_diagnostics.csv",
                index=False,
            )

        summary_records = []
        for algorithm, result in results.items():
            algorithm_dir = output_dir / algorithm
            algorithm_dir.mkdir(parents=True, exist_ok=True)
            result.edges.to_csv(algorithm_dir / "edges.csv", index=False)
            summary_records.append(
                {
                    "algorithm": algorithm,
                    "status": result.status,
                    "edges": len(result.edges),
                    "message": result.message,
                }
            )
            if result.status == "ok" and self.reporting_config.write_graph_markdown:
                self.write_algorithm_report(
                    result=result,
                    discovery_frame=discovery_frame,
                    variable_metadata=variable_metadata,
                    output_dir=algorithm_dir,
                    collinearity_threshold=collinearity_threshold,
                    campaign_id=campaign_id,
                    pre_weeks=pre_weeks,
                )

        if "pc" in results and results["pc"].status == "ok":
            pc_dir = output_dir / "pc"
            if self.reporting_config.write_alpha_sensitivity:
                alpha_summary, alpha_edges = self.diagnostics.run_pc_alpha_sensitivity(
                    standardized_frame
                )
                alpha_summary.to_csv(pc_dir / "alpha_sensitivity.csv", index=False)
                alpha_edges.to_csv(pc_dir / "alpha_sensitivity_edges.csv", index=False)

            if self.reporting_config.write_bootstrap_stability:
                stability, failures = self.diagnostics.bootstrap_pc_edge_stability(
                    standardized_frame
                )
                stability.to_csv(pc_dir / "edge_stability.csv", index=False)
                failures.to_csv(pc_dir / "bootstrap_failures.csv", index=False)

        if self.reporting_config.write_algorithm_summary:
            pd.DataFrame(summary_records).to_csv(
                output_dir / "algorithm_summary.csv",
                index=False,
            )

    def write_algorithm_report(
        self,
        *,
        result: DiscoveryResult,
        discovery_frame: pd.DataFrame,
        variable_metadata: pd.DataFrame,
        output_dir: Path,
        collinearity_threshold: float,
        campaign_id: str,
        pre_weeks: int,
    ) -> None:
        """1 アルゴリズム分の Markdown report を書き出す。

        Args:
            result: Discovery result to report.
            discovery_frame: Transformed feature frame before standardization.
            variable_metadata: Variable metadata table.
            output_dir: Algorithm-specific output directory.
            collinearity_threshold: Threshold used during preprocessing.
            campaign_id: Campaign identifier analyzed.
            pre_weeks: Number of pre-treatment weeks.
        """
        mermaid_lines = ["```mermaid", "flowchart LR"]
        mermaid_lines.extend(mermaid_edge(row) for _, row in result.edges.iterrows())
        mermaid_lines.append("```")

        used_metadata = variable_metadata.loc[variable_metadata["used_in_discovery"]]
        binary_variables = used_metadata.loc[
            used_metadata["data_type"].eq("binary"),
            "variable",
        ].tolist()
        transformed_variables = [
            f"{row.variable} ({row.transform})"
            for row in used_metadata.itertuples(index=False)
            if row.transform != "identity"
        ]
        causal_discovery = self.diagnostics.causal_discovery

        report = [
            f"# {result.algorithm.upper()} Causal Discovery",
            "",
            f"- campaign_id: `{campaign_id}`",
            f"- pre_weeks: `{pre_weeks}`",
            f"- alpha: `{causal_discovery.alpha}`",
            f"- collinearity_threshold: `{collinearity_threshold}`",
            f"- background_knowledge: `{causal_discovery.use_background_knowledge}`",
            f"- pc_indep_test: `{causal_discovery.pc_indep_test}`",
            f"- pc_discrete_bins: `{causal_discovery.pc_discrete_bins}`",
            f"- bootstrap_samples: `{causal_discovery.bootstrap_samples}`",
            f"- bootstrap_sample_fraction: `{causal_discovery.bootstrap_sample_fraction}`",
            f"- samples: `{len(discovery_frame)}`",
            f"- variables: `{len(discovery_frame.columns)}`",
            f"- edges: `{len(result.edges)}`",
            "",
            "## Graph",
            "",
            *mermaid_lines,
            "",
            "## Edges",
            "",
            dataframe_to_markdown(result.edges),
            "",
            "## Data and Test Assumptions",
            "",
            f"- binary_variables: `{', '.join(binary_variables) or 'none'}`",
            f"- transformed_variables: `{', '.join(transformed_variables) or 'none'}`",
            "- count and monetary/discount variables are transformed before standardization; non-negative variables use log1p and signed discount-like variables use signed_log1p.",
            "- Fisher-z PC should be interpreted as a partial-correlation conditional-independence search when binary, ordinal-midpoint, numeric-category, count, or zero-inflated monetary variables are included.",
            "- `--pc-indep-test kci` is available as a nonlinear CI alternative, but it is not a complete mixed-type solution for binary plus continuous data.",
            "- `--pc-indep-test gsq` or `chisq` is available for a discrete-data sensitivity run; continuous variables are quantile-discretized with `--pc-discrete-bins`.",
            "- A proper mixed-type CI test is not implemented in this dependency set; treat that as a remaining methodological limitation rather than solved by standardization.",
            "- PC alpha sensitivity is written to `pc/alpha_sensitivity.csv` and `pc/alpha_sensitivity_edges.csv` when PC succeeds.",
            "- PC bootstrap edge stability is written to `pc/edge_stability.csv` when PC succeeds and `--bootstrap-samples` is positive.",
            "",
            "## Interpretation",
            "",
            "- PC は条件付き独立性から CPDAG を推定する制約ベース手法。",
            "- GES はスコアを改善する貪欲探索で等価クラスを推定するスコアベース手法。",
            "- LiNGAM は線形・非 Gaussian・非巡回などの仮定を使って向き付き構造を推定する。",
            "- NOTEARS は DAG 制約を連続最適化問題として扱う。",
        ]
        (output_dir / "graph.md").write_text("\n".join(report), encoding="utf-8")
