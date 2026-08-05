"""Generic single-table execution path for Web analysis-ready datasets."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd
from sqlalchemy import select
from sqlalchemy.orm import Session

from ariadne.causal.discovery.algorithms import CausalDiscovery
from ariadne.causal.inference.estimators.edge_weight import EdgeWeightEstimator
from ariadne.causal.inference.estimators.treatment_effect import (
    TreatmentEffectEstimator,
)
from ariadne.application.ports import ArtifactLocation
from ariadne.domain import metadata as m
from ariadne.preprocessing.discovery.config import (
    BackgroundKnowledgeConfig,
    FeatureConfig,
)


class AnalysisReadyExecutor:
    """Condition and analyze one immutable Dataset Table Version directly."""

    def __init__(self, store: Any) -> None:
        self.store = store

    def execute(
        self,
        session: Session,
        stage: m.StageExecution,
        output_dir: Path,
        parameters: dict[str, Any],
    ) -> tuple[dict[str, Path], dict[str, Any]]:
        preparation = session.get(m.StageExecutionInputPreparation, stage.id)
        if not preparation or not preparation.input_table_version_id:
            raise ValueError("ANALYSIS_READY input preparation is missing")
        table = session.get(m.DatasetTableVersion, preparation.input_table_version_id)
        stored = session.get(m.StoredObject, table.stored_object_id)
        path = self.store.resolve_local_path(
            ArtifactLocation(
                backend=stored.backend,
                namespace=stored.bucket,
                key=stored.object_key,
                version=stored.object_version or None,
            )
        )
        frame = (
            pd.read_csv(path)
            if table.file_format == "CSV"
            else pd.read_parquet(path)
        )
        semantics = session.scalars(
            select(m.FeatureSemanticItem).where(
                m.FeatureSemanticItem.feature_semantics_version_id
                == preparation.feature_semantics_version_id
            )
        ).all()
        conditioned, original, excluded, resolved = self._condition(
            frame, semantics, parameters, stage.stage_type
        )
        output_dir.mkdir(parents=True, exist_ok=True)
        feature_frame = output_dir / "analysis_ready_feature_frame.parquet"
        conditioned.to_parquet(feature_frame, index=False)
        preparation_path = output_dir / "input_preparation.json"
        preparation_path.write_text(
            json.dumps(
                {
                    "input_mode": "ANALYSIS_READY",
                    "selected_columns": list(conditioned.columns),
                    "excluded_columns": excluded,
                    "resolved_conditioning": resolved,
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )
        if stage.stage_type == "DISCOVERY":
            artifacts = self._discovery(conditioned, output_dir, parameters)
        elif stage.analysis_mode == "EDGE_WEIGHT":
            artifacts = self._edge_weight(
                session, stage, conditioned, original, output_dir, parameters
            )
        elif stage.analysis_mode == "TREATMENT_EFFECT":
            artifacts = self._treatment_effect(
                session, stage, original, output_dir, parameters
            )
        else:
            raise ValueError(f"Unsupported ANALYSIS_READY stage: {stage.stage_type}")
        for config_input in session.scalars(
            select(m.StageExecutionConfigInput).where(
                m.StageExecutionConfigInput.stage_execution_id == stage.id
            )
        ).all():
            version = session.get(
                m.ConfigurationVersion, config_input.configuration_version_id
            )
            resolved_path = output_dir / f"resolved_{config_input.input_name}.json"
            resolved_path.write_text(
                json.dumps(
                    version.canonical_json,
                    ensure_ascii=False,
                    sort_keys=True,
                    indent=2,
                ),
                encoding="utf-8",
            )
            artifacts[f"resolved_{config_input.input_name}"] = resolved_path
        artifacts.update(
            {"feature_frame": feature_frame, "input_preparation": preparation_path}
        )
        return artifacts, {
            "actual_selected_columns_json": list(conditioned.columns),
            "excluded_columns_json": excluded,
            "resolved_conditioning_json": resolved,
        }

    def _condition(
        self,
        frame: pd.DataFrame,
        semantics: list[m.FeatureSemanticItem],
        parameters: dict[str, Any],
        stage_type: str,
    ) -> tuple[pd.DataFrame, pd.DataFrame, list[dict[str, str]], dict[str, Any]]:
        requested = parameters.get("selected_columns") or [
            item.name
            for item in semantics
            if item.allowed_for_discovery
            and item.role not in {"identifier", "excluded", "post_treatment"}
        ]
        by_name = {item.name: item for item in semantics}
        missing = [name for name in requested if name not in by_name]
        if missing:
            raise ValueError(f"Selected columns are absent from Feature Semantics: {missing}")
        source_names = [by_name[name].source_column or name for name in requested]
        absent = [name for name in source_names if name not in frame.columns]
        if absent:
            raise ValueError(f"Selected source columns are absent from Dataset: {absent}")
        selected = frame.loc[:, source_names].copy()
        selected.columns = requested
        conditioning = parameters.get("conditioning", {})
        categorical_policy = conditioning.get("categorical_encoding", "ordinal")
        excluded: list[dict[str, str]] = []
        for name in list(selected.columns):
            item = by_name[name]
            if item.categorical or not pd.api.types.is_numeric_dtype(selected[name]):
                if categorical_policy == "reject":
                    raise ValueError(f"Categorical column requires an encoding policy: {name}")
                selected[name] = pd.Categorical(selected[name]).codes.astype(float)
                selected.loc[selected[name] < 0, name] = pd.NA
            else:
                selected[name] = pd.to_numeric(selected[name], errors="coerce")
        missing_policy = conditioning.get("missing_values", "complete_case")
        if missing_policy == "median":
            selected = selected.fillna(selected.median(numeric_only=True))
        elif missing_policy == "complete_case":
            selected = selected.dropna()
        else:
            raise ValueError(f"Unsupported missing-value policy: {missing_policy}")
        for name in list(selected.columns):
            if selected[name].nunique(dropna=True) <= 1:
                selected = selected.drop(columns=[name])
                excluded.append({"column": name, "reason": "constant"})
        threshold = float(conditioning.get("collinearity_threshold", 0.995))
        correlations = selected.corr(numeric_only=True).abs()
        for index, name in enumerate(list(correlations.columns)):
            if name not in selected:
                continue
            prior = list(correlations.columns[:index])
            if any(
                other in selected and correlations.loc[name, other] > threshold
                for other in prior
            ):
                selected = selected.drop(columns=[name])
                excluded.append({"column": name, "reason": "collinear"})
        if selected.shape[1] < 2:
            raise ValueError("At least two non-constant analysis columns are required")
        original = selected.copy()
        standardize = bool(conditioning.get("standardize", stage_type == "DISCOVERY"))
        if standardize:
            selected = (selected - selected.mean()) / selected.std(ddof=0)
        return selected, original, excluded, {
            "missing_values": missing_policy,
            "categorical_encoding": categorical_policy,
            "standardize": standardize,
            "constant_columns": "exclude",
            "collinearity_threshold": threshold,
        }

    def _discovery(
        self, frame: pd.DataFrame, output_dir: Path, parameters: dict[str, Any]
    ) -> dict[str, Path]:
        algorithms = tuple(parameters.get("algorithms", ["pc", "ges", "lingam"]))
        unsupported = set(algorithms) - {"pc", "ges", "lingam"}
        if unsupported:
            raise ValueError(f"Unsupported discovery algorithms: {sorted(unsupported)}")
        empty_features = FeatureConfig(
            metadata={},
            tables={},
            campaign_window={},
            categorical_mappings={},
            features={},
            background_knowledge=BackgroundKnowledgeConfig(tier_order=()),
        )
        discovery = CausalDiscovery(
            alpha=float(parameters.get("alpha", 0.01)),
            use_background_knowledge=False,
            feature_config=empty_features,
            algorithms=algorithms,
            bootstrap_samples=0,
            random_seed=int(parameters.get("random_seed", 20260630)),
            ges_max_p=int(parameters["ges_max_p"]) if "ges_max_p" in parameters else None,
            ges_score_func=str(parameters.get("ges_score_func", "local_score_BIC")),
        )
        results = discovery.run_all(frame)
        summaries: list[dict[str, Any]] = []
        artifacts: dict[str, Path] = {}
        for algorithm, result in results.items():
            algorithm_dir = output_dir / algorithm
            algorithm_dir.mkdir(parents=True, exist_ok=True)
            edge_path = algorithm_dir / "edges.csv"
            result.edges.to_csv(edge_path, index=False)
            artifacts[f"{algorithm}_edges"] = edge_path
            summaries.append(
                {
                    "algorithm": algorithm,
                    "status": result.status,
                    "edges": len(result.edges),
                    "message": result.message,
                }
            )
        summary_path = output_dir / "algorithm_summary.csv"
        pd.DataFrame(summaries).to_csv(summary_path, index=False)
        artifacts["algorithm_summary"] = summary_path
        diagnostics_path = output_dir / "variable_diagnostics.csv"
        frame.describe().transpose().reset_index(names="variable").to_csv(
            diagnostics_path, index=False
        )
        artifacts["variable_diagnostics"] = diagnostics_path
        report_path = output_dir / "discovery_report.md"
        report_path.write_text(
            "# Analysis-ready causal discovery\n\n"
            "The reported structures are algorithm-dependent hypotheses, not a proven true DAG.\n",
            encoding="utf-8",
        )
        artifacts["report"] = report_path
        return artifacts

    def _edge_weight(
        self,
        session: Session,
        stage: m.StageExecution,
        standardized: pd.DataFrame,
        original: pd.DataFrame,
        output_dir: Path,
        parameters: dict[str, Any],
    ) -> dict[str, Path]:
        graph = self._graph_version(session, stage)
        graph_dir = output_dir / "saved_graph" / graph.algorithm
        graph_dir.mkdir(parents=True, exist_ok=True)
        edge_rows = []
        for edge in session.scalars(
            select(m.CausalGraphEdge).where(
                m.CausalGraphEdge.causal_graph_version_id == graph.id
            )
        ).all():
            symbol = _edge_symbol(edge.endpoint_at_a, edge.endpoint_at_b)
            edge_rows.append(
                {"source": edge.node_a, "target": edge.node_b, "edge": symbol}
            )
        pd.DataFrame(edge_rows, columns=["source", "target", "edge"]).to_csv(
            graph_dir / "edges.csv", index=False
        )
        estimator = EdgeWeightEstimator(
            standardized_frame=standardized,
            original_frame=original,
            discovery_dir=output_dir / "saved_graph",
            output_dir=output_dir,
            algorithms=(graph.algorithm,),
            dropped_columns=pd.DataFrame(columns=["column", "reason"]),
            robust_se=str(parameters.get("edge_robust_se", "HC3")),
            min_samples=int(parameters.get("min_samples", 30)),
        )
        effects, skipped = estimator.estimate_all_edge_coefficients()
        effects = effects.rename(
            columns={
                "coefficient_original_scale": "coefficient",
                "standard_error_original_scale": "standard_error",
                "ci_low_original_scale": "ci_lower",
                "ci_high_original_scale": "ci_upper",
                "n_samples": "sample_count",
            }
        )
        effects["status"] = "OK"
        effects["robust_se"] = str(parameters.get("edge_robust_se", "HC3"))
        path = output_dir / "edge_effects.csv"
        effects.to_csv(path, index=False)
        skipped_path = output_dir / "skipped_edges.csv"
        skipped.to_csv(skipped_path, index=False)
        report = output_dir / "edge_weight_report.md"
        report.write_text(
            "# Exploratory edge coefficients\n\n"
            "These coefficients are not identified causal effects.\n",
            encoding="utf-8",
        )
        return {"edge_effects": path, "skipped_edges": skipped_path, "report": report}

    def _treatment_effect(
        self,
        session: Session,
        stage: m.StageExecution,
        frame: pd.DataFrame,
        output_dir: Path,
        parameters: dict[str, Any],
    ) -> dict[str, Path]:
        configs = {
            row.input_name: row.configuration_version_id
            for row in session.scalars(
                select(m.StageExecutionConfigInput).where(
                    m.StageExecutionConfigInput.stage_execution_id == stage.id
                )
            ).all()
        }
        design = session.get(m.CausalDesignProjection, configs.get("causal_design"))
        if not design:
            raise ValueError("A projected Causal Design is required")
        covariates = list(design.adjustment_set_json or parameters.get("covariates", []))
        estimator = TreatmentEffectEstimator(
            frame=frame,
            treatment=design.treatment_name,
            outcome=design.outcome_name,
            covariates=covariates,
            estimand=design.estimand,
            robust_se=str(parameters.get("robust_se", "HC3")),
        )
        default_methods = [
            "diff_in_means",
            "ols_coefficient",
            "g_computation_ate" if design.estimand == "ATE" else "g_computation_att",
        ]
        results = estimator.estimate(parameters.get("effect_methods", default_methods))
        results = results.rename(
            columns={
                "effect": "estimate",
                "std_error": "standard_error",
                "ci_low": "ci_lower",
                "ci_high": "ci_upper",
                "n": "sample_count",
            }
        )
        path = output_dir / "treatment_effects.csv"
        results.to_csv(path, index=False)
        selected = output_dir / "selected_adjustment_set.csv"
        pd.DataFrame(
            [{"feature_name": name, "selection_source": "CAUSAL_DESIGN"} for name in covariates]
        ).to_csv(selected, index=False)
        diagnostics = output_dir / "design_diagnostics.csv"
        pd.DataFrame(
            [
                {
                    "treatment": design.treatment_name,
                    "outcome": design.outcome_name,
                    "estimand": design.estimand,
                    "sample_count": len(frame),
                }
            ]
        ).to_csv(diagnostics, index=False)
        report = output_dir / "treatment_effect_report.md"
        report.write_text(
            "# Treatment-effect estimates\n\n"
            "Interpret estimates under the declared consistency, exchangeability, and positivity assumptions.\n",
            encoding="utf-8",
        )
        return {
            "treatment_effects": path,
            "selected_adjustment_set": selected,
            "design_diagnostics": diagnostics,
            "report": report,
        }

    @staticmethod
    def _graph_version(session: Session, stage: m.StageExecution) -> m.CausalGraphVersion:
        graph_input = session.scalar(
            select(m.StageExecutionGraphInput).where(
                m.StageExecutionGraphInput.stage_execution_id == stage.id
            )
        )
        if not graph_input:
            raise ValueError("Saved Graph input is required")
        return session.get(m.CausalGraphVersion, graph_input.causal_graph_version_id)


def _edge_symbol(endpoint_a: str, endpoint_b: str) -> str:
    return {
        ("TAIL", "ARROW"): "-->",
        ("TAIL", "TAIL"): "---",
        ("ARROW", "ARROW"): "<->",
        ("CIRCLE", "ARROW"): "o->",
        ("CIRCLE", "CIRCLE"): "o-o",
    }.get((endpoint_a, endpoint_b), "---")


__all__ = ["AnalysisReadyExecutor"]
