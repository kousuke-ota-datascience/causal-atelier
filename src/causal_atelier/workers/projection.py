"""Project worker query/profile results into durable metadata."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
from sqlalchemy import select
from sqlalchemy.orm import Session

from causal_atelier.application.ports import ArtifactStore, DataQuery
from causal_atelier.application.visualization import complete_visualization_query
from causal_atelier.infrastructure.artifact_store import artifact_location
from causal_atelier.infrastructure.persistence import models as m


class WorkerProjectionService:
    def __init__(self, store: ArtifactStore, query_engine: DataQuery) -> None:
        self.store = store
        self.query_engine = query_engine

    def profile_table(self, session: Session, table_id: str, profile_id: str) -> None:
        table = session.get(m.DatasetTableVersion, table_id)
        profile = session.get(m.DataProfile, profile_id)
        if not table or not profile or profile.status == "SUCCEEDED":
            return
        stored = session.get(m.StoredObject, table.stored_object_id)
        profile.status = "RUNNING"
        session.commit()
        try:
            summary = self.query_engine.profile(
                self.store.resolve_local_path(artifact_location(stored)),
                table.file_format,
            )
            profile.status = "SUCCEEDED"
            profile.summary_json = summary
            profile.sampled = bool(summary.get("sampled", False))
            profile.sample_size = summary.get("sample_size")
            table.row_count = summary["row_count"]
            table.column_count = summary["column_count"]
            columns = session.scalars(
                select(m.DatasetColumn).where(
                    m.DatasetColumn.dataset_table_version_id == table.id
                )
            ).all()
            by_name = {column.name: column for column in columns}
            for item in summary["columns"]:
                column = by_name[item["name"]]
                session.merge(
                    m.ColumnProfile(
                        data_profile_id=profile.id,
                        dataset_column_id=column.id,
                        null_count=item["null_count"],
                        distinct_count=item["distinct_count"],
                        min_value=None if item["min"] is None else str(item["min"]),
                        max_value=None if item["max"] is None else str(item["max"]),
                        statistics_json=item["statistics"],
                    )
                )
        except Exception as exc:
            profile.status = "FAILED"
            profile.error_summary = str(exc)[:4000]

    def execute_visualization_query(self, session: Session, query_id: str) -> None:
        query = session.get(m.VisualizationQuery, query_id)
        if not query or query.status in {"SUCCEEDED", "FAILED", "CANCELLED"}:
            return
        table = session.get(m.DatasetTableVersion, query.dataset_table_version_id)
        stored = session.get(m.StoredObject, table.stored_object_id)
        query.status = "RUNNING"
        query.started_at = m.utcnow()
        session.commit()
        try:
            result = self.query_engine.execute(
                self.store.resolve_local_path(artifact_location(stored)),
                table.file_format,
                query.query_json,
            )
            complete_visualization_query(session, query, table, result.to_dict())
        except Exception as exc:
            query.status = "FAILED"
            query.error_summary = str(exc)[:4000]
            query.finished_at = m.utcnow()

    def project_results(
        self,
        session: Session,
        stage: m.StageRun,
        artifacts: dict[str, Path],
        output_dir: Path,
    ) -> None:
        if stage.stage_type == "DISCOVERY":
            self._project_discovery(session, stage, output_dir)
        elif stage.analysis_mode == "EDGE_WEIGHT":
            self._project_edge_weights(session, stage, artifacts)
        elif stage.analysis_mode == "TREATMENT_EFFECT":
            self._project_treatment_effects(session, stage, artifacts)

    def _project_discovery(
        self, session: Session, stage: m.StageRun, output_dir: Path
    ) -> None:
        configs = _config_id_map(session, stage.id)
        dataset_id = _first_dataset_id(session, stage.id)
        required = (
            configs.get("analysis_config") or configs.get("config"),
            configs.get("feature_config"),
            dataset_id,
        )
        if not all(required):
            return
        summary_path = output_dir / "algorithm_summary.csv"
        summaries = (
            pd.read_csv(summary_path).to_dict("records")
            if summary_path.exists()
            else []
        )
        result = m.DiscoveryResult(
            stage_run_id=stage.id,
            dataset_version_id=dataset_id,
            discovery_analysis_version_id=required[0],
            discovery_feature_version_id=required[1],
            algorithm_count=len(summaries),
            node_count=None,
            edge_count=0,
            status="SUCCEEDED",
            summary_json={
                "scientific_notice": "Algorithm-dependent exploratory structure"
            },
        )
        session.add(result)
        session.flush()
        total = 0
        for summary in summaries:
            algorithm = str(summary["algorithm"])
            edge_path = output_dir / algorithm / "edges.csv"
            algorithm_result = m.DiscoveryAlgorithmResult(
                discovery_result_id=result.id,
                algorithm=algorithm,
                status=str(summary.get("status", "unknown")).upper(),
                message=None
                if pd.isna(summary.get("message"))
                else str(summary.get("message")),
                metadata_json={"edge_count": int(summary.get("edges", 0))},
            )
            session.add(algorithm_result)
            session.flush()
            if edge_path.exists():
                for raw in pd.read_csv(edge_path).to_dict("records"):
                    source = raw.pop("source", raw.pop("from", None))
                    target = raw.pop("target", raw.pop("to", None))
                    if source is None or target is None:
                        continue
                    session.add(
                        m.DiscoveryEdge(
                            discovery_algorithm_result_id=algorithm_result.id,
                            source=str(source),
                            target=str(target),
                            edge_type=_nullable_string(raw.pop("edge_type", None)),
                            orientation=_nullable_string(raw.pop("orientation", None)),
                            score=_nullable_float(raw.pop("score", None)),
                            stability=_nullable_float(raw.pop("stability", None)),
                            selected=True,
                            payload_json=_json_safe(raw),
                        )
                    )
                    total += 1
        result.edge_count = total

    def _project_edge_weights(
        self, session: Session, stage: m.StageRun, artifacts: dict[str, Path]
    ) -> None:
        path = artifacts.get("edge_effects")
        if not path or not path.exists():
            return
        artifact = _artifact_for_output(session, stage.id, "edge_effects")
        configs = _config_id_map(session, stage.id)
        analysis = configs.get("analysis_config") or configs.get("config")
        features = configs.get("feature_config")
        dataset_id = _first_dataset_id(session, stage.id)
        if not all((artifact, analysis, features, dataset_id)):
            return
        result = m.EdgeWeightResult(
            stage_run_id=stage.id,
            dataset_version_id=dataset_id,
            inference_analysis_version_id=analysis,
            inference_feature_version_id=features,
            result_artifact_id=artifact.id,
            status="SUCCEEDED",
            summary_json={"interpretation_level": "EXPLORATORY_EDGE_COEFFICIENT"},
        )
        session.add(result)
        session.flush()
        for raw in pd.read_csv(path).to_dict("records"):
            session.add(
                m.EdgeWeightEstimate(
                    edge_weight_result_id=result.id,
                    algorithm=str(raw.get("algorithm", "unknown")),
                    source=str(raw.get("source", "")),
                    target=str(raw.get("target", "")),
                    coefficient=_nullable_float(raw.get("coefficient")),
                    standard_error=_nullable_float(
                        raw.get("standard_error", raw.get("std_error"))
                    ),
                    statistic=_nullable_float(raw.get("statistic")),
                    p_value=_nullable_float(raw.get("p_value")),
                    adjusted_p_value=_nullable_float(raw.get("adjusted_p_value")),
                    ci_lower=_nullable_float(raw.get("ci_lower")),
                    ci_upper=_nullable_float(raw.get("ci_upper")),
                    sample_count=_nullable_int(raw.get("sample_count", raw.get("n"))),
                    robust_se=_nullable_string(raw.get("robust_se")),
                    status=str(raw.get("status", "ok")).upper(),
                    warning=_nullable_string(raw.get("warning")),
                    payload_json=_json_safe(raw),
                )
            )

    def _project_treatment_effects(
        self, session: Session, stage: m.StageRun, artifacts: dict[str, Path]
    ) -> None:
        path = artifacts.get("treatment_effects")
        if not path or not path.exists():
            return
        artifact = _artifact_for_output(session, stage.id, "treatment_effects")
        configs = _config_id_map(session, stage.id)
        analysis = configs.get("analysis_config") or configs.get("config")
        features = configs.get("feature_config")
        semantics = configs.get("feature_semantics")
        design_id = configs.get("causal_design")
        dataset_id = _first_dataset_id(session, stage.id)
        design = session.get(m.CausalDesignProjection, design_id) if design_id else None
        if not all(
            (artifact, analysis, features, semantics, design_id, dataset_id, design)
        ):
            return
        params = {
            row.parameter_name: row.value_json
            for row in session.scalars(
                select(m.StageRunParameter).where(
                    m.StageRunParameter.stage_run_id == stage.id
                )
            ).all()
        }
        result = m.TreatmentEffectResult(
            stage_run_id=stage.id,
            dataset_version_id=dataset_id,
            inference_analysis_version_id=analysis,
            inference_feature_version_id=features,
            feature_semantics_version_id=semantics,
            causal_design_version_id=design_id,
            treatment_name=design.treatment_name,
            outcome_name=design.outcome_name,
            estimand=design.estimand,
            adjustment_strategy=str(
                params.get("adjustment_strategy", "pre_treatment_covariates")
            ),
            result_artifact_id=artifact.id,
            diagnostic_status="AVAILABLE",
            summary_json={"assumptions_are_declarations": True},
        )
        session.add(result)
        session.flush()
        for raw in pd.read_csv(path).to_dict("records"):
            session.add(
                m.TreatmentEffectEstimate(
                    treatment_effect_result_id=result.id,
                    method=str(raw.get("method", "unknown")),
                    estimand=str(raw.get("estimand", design.estimand)),
                    estimate=_nullable_float(raw.get("estimate")),
                    standard_error=_nullable_float(raw.get("standard_error")),
                    ci_lower=_nullable_float(raw.get("ci_lower")),
                    ci_upper=_nullable_float(raw.get("ci_upper")),
                    p_value=_nullable_float(raw.get("p_value")),
                    adjusted_p_value=_nullable_float(raw.get("adjusted_p_value")),
                    sample_count=_nullable_int(raw.get("sample_count", raw.get("n"))),
                    effective_sample_size=_nullable_float(
                        raw.get("effective_sample_size")
                    ),
                    robust_se=_nullable_string(raw.get("robust_se")),
                    adjustment_method=_nullable_string(raw.get("adjustment_method")),
                    diagnostic_status=str(raw.get("diagnostic_status", "AVAILABLE")),
                    notes=_nullable_string(raw.get("notes")),
                    warnings=_nullable_string(raw.get("warnings")),
                    payload_json=_json_safe(raw),
                )
            )
        selected_path = path.parent / "selected_adjustment_set.csv"
        if selected_path.exists():
            for ordinal, raw in enumerate(
                pd.read_csv(selected_path).to_dict("records"), start=1
            ):
                name = raw.get("feature_name", raw.get("variable"))
                if name:
                    session.add(
                        m.SelectedAdjustmentVariable(
                            treatment_effect_result_id=result.id,
                            feature_name=str(name),
                            ordinal=ordinal,
                            selection_source=str(
                                raw.get("selection_source", "PRE_TREATMENT_CONFIG")
                            ),
                        )
                    )


def _first_dataset_id(session: Session, stage_id: str) -> str | None:
    return session.scalar(
        select(m.StageRunDatasetInput.dataset_version_id).where(
            m.StageRunDatasetInput.stage_run_id == stage_id
        )
    )


def _config_id_map(session: Session, stage_id: str) -> dict[str, str]:
    return {
        item.input_name: item.configuration_version_id
        for item in session.scalars(
            select(m.StageRunConfigInput).where(
                m.StageRunConfigInput.stage_run_id == stage_id
            )
        ).all()
    }


def _artifact_for_output(
    session: Session, stage_id: str, name: str
) -> m.Artifact | None:
    output = session.get(m.StageRunArtifactOutput, (stage_id, name))
    return session.get(m.Artifact, output.artifact_id) if output else None


def _nullable_float(value: object) -> float | None:
    return None if value is None or pd.isna(value) else float(value)


def _nullable_int(value: object) -> int | None:
    return None if value is None or pd.isna(value) else int(value)


def _nullable_string(value: object) -> str | None:
    return None if value is None or pd.isna(value) else str(value)


def _json_safe(document: dict[str, object]) -> dict[str, object]:
    return json.loads(
        json.dumps(
            document, default=lambda value: None if pd.isna(value) else str(value)
        )
    )


__all__ = ["WorkerProjectionService"]
