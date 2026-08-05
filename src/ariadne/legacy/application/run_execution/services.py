"""Run execution use cases and shared control-plane policies."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import yaml
from sqlalchemy import func, select

from ariadne.application.ports import ArtifactStore, DataQuery, MetadataRepository
from ariadne.domain import metadata as m


class ConflictError(ValueError):
    pass


class ResourceNotFoundError(ValueError):
    pass


class ValidationError(ValueError):
    def __init__(self, issues: list[dict[str, Any]]) -> None:
        self.issues = issues
        super().__init__("; ".join(issue["message"] for issue in issues))


def canonical_hash(document: Any) -> str:
    payload = json.dumps(
        document, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def add_audit(
    session: MetadataRepository,
    *,
    project_id: str | None,
    actor_user_id: str | None,
    action: str,
    resource_type: str,
    resource_id: str | None,
    request_id: str | None = None,
    before: dict[str, Any] | None = None,
    after: dict[str, Any] | None = None,
) -> None:
    session.add(
        m.AuditEvent(
            project_id=project_id,
            actor_user_id=actor_user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            request_id=request_id,
            before_json=before,
            after_json=after,
        )
    )


class _DataCatalogService:
    def __init__(
        self,
        session: MetadataRepository,
        store: ArtifactStore,
        query_engine: DataQuery,
    ) -> None:
        self.session = session
        self.store = store
        self.query_engine = query_engine

    def create_version(
        self,
        *,
        dataset: m.Dataset,
        actor_user_id: str,
        source_type: str,
        source_metadata: dict[str, Any],
        tables: list[dict[str, Any]],
        profile: bool,
    ) -> m.DatasetVersion:
        version_number = (
            self.session.scalar(
                select(func.max(m.DatasetVersion.version_number)).where(
                    m.DatasetVersion.dataset_id == dataset.id
                )
            )
            or 0
        ) + 1
        version = m.DatasetVersion(
            dataset_id=dataset.id,
            version_number=version_number,
            status="REGISTERING",
            source_type=source_type,
            source_metadata=source_metadata,
            table_count=len(tables),
            created_by=actor_user_id,
        )
        self.session.add(version)
        self.session.flush()
        table_hashes: list[dict[str, Any]] = []
        schema_hashes: list[dict[str, Any]] = []
        for ordinal, raw in enumerate(tables, start=1):
            object_data = raw["object"]
            if object_data["backend"] != self.store.backend:
                raise ValidationError(
                    [
                        _issue(
                            "unsupported_backend",
                            f"This deployment uses {self.store.backend} storage",
                        )
                    ]
                )
            if object_data.get("namespace") != self.store.namespace:
                raise ValidationError(
                    [
                        _issue(
                            "namespace_mismatch",
                            "Object reference does not belong to this deployment",
                        )
                    ]
                )
            path = self.store.resolve_local_path(object_data["key"])
            actual_checksum = _hash_file(path)
            if actual_checksum != object_data["checksum"]:
                raise ValidationError(
                    [
                        _issue(
                            "checksum_mismatch",
                            f"Checksum mismatch for {raw['logical_name']}",
                        )
                    ]
                )
            file_format = object_data["format"].upper()
            schema = (
                self.query_engine.schema(path, file_format)
                if file_format in {"CSV", "PARQUET"}
                else []
            )
            schema_hash = canonical_hash(schema)
            stored = self.session.scalar(
                select(m.StoredObject).where(
                    m.StoredObject.backend == self.store.backend,
                    m.StoredObject.bucket == object_data.get("namespace"),
                    m.StoredObject.object_key == object_data["key"],
                    m.StoredObject.object_version == (object_data.get("version") or ""),
                )
            )
            if stored is None:
                stored = m.StoredObject(
                    backend=self.store.backend,
                    bucket=object_data.get("namespace"),
                    object_key=object_data["key"],
                    object_version=object_data.get("version") or "",
                    media_type=object_data.get("media_type"),
                    format=file_format,
                    size_bytes=path.stat().st_size,
                    checksum=actual_checksum,
                    status="AVAILABLE",
                )
                self.session.add(stored)
                self.session.flush()
            table = m.DatasetTableVersion(
                dataset_version_id=version.id,
                logical_name=raw["logical_name"],
                stored_object_id=stored.id,
                ordinal=ordinal,
                file_format=file_format,
                row_count=None,
                column_count=len(schema),
                schema_json={"fields": schema},
                schema_hash=schema_hash,
                content_hash=actual_checksum,
                partition_values=raw.get("partition_values"),
                source_entry_name=raw.get("source_entry_name"),
            )
            self.session.add(table)
            self.session.flush()
            for column_ordinal, column in enumerate(schema, start=1):
                dataset_column = m.DatasetColumn(
                    dataset_table_version_id=table.id,
                    ordinal=column_ordinal,
                    name=column["name"],
                    physical_type=column["physical_type"],
                    logical_type=column["logical_type"],
                    nullable=column["nullable"],
                )
                self.session.add(dataset_column)
                self.session.flush()
                self.session.add(
                    m.DatasetColumnPolicy(
                        dataset_column_id=dataset_column.id,
                        classification="INTERNAL",
                        preview_allowed=True,
                        analysis_allowed=True,
                        download_allowed=True,
                        updated_by=actor_user_id,
                    )
                )
            if profile and file_format in {"CSV", "PARQUET"}:
                data_profile = m.DataProfile(
                    dataset_table_version_id=table.id, status="PENDING"
                )
                self.session.add(data_profile)
                self.session.flush()
                self.session.add(
                    m.OutboxEvent(
                        aggregate_type="DATASET_TABLE_VERSION",
                        aggregate_id=table.id,
                        event_type="PROFILE_DATASET_TABLE",
                        payload_json={
                            "dataset_table_version_id": table.id,
                            "profile_id": data_profile.id,
                        },
                    )
                )
            table_hashes.append(
                {"logical_name": table.logical_name, "hash": actual_checksum}
            )
            schema_hashes.append(
                {"logical_name": table.logical_name, "schema_hash": schema_hash}
            )
        version.schema_hash = canonical_hash(schema_hashes)
        version.content_hash = canonical_hash(table_hashes)
        version.status = "READY"
        version.ready_at = m.utcnow()
        if len(tables) == 1 and tables[0]["object"]["format"].upper() in {
            "CSV",
            "PARQUET",
        }:
            primary_table = self.session.scalar(
                select(m.DatasetTableVersion).where(
                    m.DatasetTableVersion.dataset_version_id == version.id
                )
            )
            self.session.add(
                m.AnalysisDatasetBinding(
                    dataset_version_id=version.id,
                    primary_table_version_id=primary_table.id,
                    analysis_unit_description=source_metadata.get(
                        "analysis_unit_description", "One row is one analysis unit"
                    ),
                    readiness_status="READY",
                    schema_hash_snapshot=version.schema_hash,
                    validation_summary_json={"issues": []},
                    created_by=actor_user_id,
                    validated_at=m.utcnow(),
                )
            )
        add_audit(
            self.session,
            project_id=dataset.project_id,
            actor_user_id=actor_user_id,
            action="DATASET_VERSION_CREATE",
            resource_type="DATASET_VERSION",
            resource_id=version.id,
            after={
                "version_number": version.version_number,
                "content_hash": version.content_hash,
            },
        )
        return version

    def registry_snapshot(self, version: m.DatasetVersion) -> dict[str, Any]:
        tables = self.session.scalars(
            select(m.DatasetTableVersion)
            .where(m.DatasetTableVersion.dataset_version_id == version.id)
            .order_by(m.DatasetTableVersion.ordinal)
        ).all()
        result: dict[str, Any] = {
            "schema_version": "2",
            "dataset_version_id": version.id,
            "content_hash": version.content_hash,
            "tables": {},
        }
        for table in tables:
            stored = self.session.get(m.StoredObject, table.stored_object_id)
            result["tables"][table.logical_name] = {
                "artifact_uri": f"artifact://{stored.id}",
                "format": table.file_format.lower(),
                "checksum": table.content_hash,
            }
        return result


class _ConfigurationService:
    def __init__(self, session: MetadataRepository) -> None:
        self.session = session

    def create_version(
        self,
        configuration: m.Configuration,
        *,
        actor_user_id: str,
        canonical_json: dict[str, Any] | None,
        yaml_text: str | None,
        schema_version: str,
    ) -> m.ConfigurationVersion:
        if yaml_text is not None:
            loaded = yaml.safe_load(yaml_text)
            if not isinstance(loaded, dict):
                raise ValidationError(
                    [
                        _issue(
                            "configuration_not_mapping",
                            "Configuration must be a mapping",
                        )
                    ]
                )
            document = loaded
            original_format = "YAML"
        else:
            document = canonical_json or {}
            original_format = "JSON"
        digest = canonical_hash(document)
        existing = self.session.scalar(
            select(m.ConfigurationVersion).where(
                m.ConfigurationVersion.configuration_id == configuration.id,
                m.ConfigurationVersion.content_hash == digest,
            )
        )
        if existing:
            raise ConflictError(
                f"Identical configuration already exists as version {existing.version_number}"
            )
        number = (
            self.session.scalar(
                select(func.max(m.ConfigurationVersion.version_number)).where(
                    m.ConfigurationVersion.configuration_id == configuration.id
                )
            )
            or 0
        ) + 1
        issues = validate_configuration(configuration.configuration_type, document)
        issues.extend(
            self._validate_resource_bindings(
                configuration.project_id, configuration.configuration_type, document
            )
        )
        version = m.ConfigurationVersion(
            configuration_id=configuration.id,
            version_number=number,
            status="DRAFT",
            schema_version=schema_version,
            canonical_json=document,
            original_format=original_format,
            original_text=yaml_text,
            content_hash=digest,
            validation_status="INVALID"
            if any(i["severity"] == "ERROR" for i in issues)
            else "VALID",
            validation_summary={"issues": issues},
            created_by=actor_user_id,
        )
        self.session.add(version)
        self.session.flush()
        if version.validation_status == "VALID":
            self._project(configuration.configuration_type, version, document)
        add_audit(
            self.session,
            project_id=configuration.project_id,
            actor_user_id=actor_user_id,
            action="CONFIGURATION_VERSION_CREATE",
            resource_type="CONFIGURATION_VERSION",
            resource_id=version.id,
            after={"version_number": number, "content_hash": digest},
        )
        return version

    def validate(
        self, configuration: m.Configuration, version: m.ConfigurationVersion
    ) -> list[dict[str, Any]]:
        issues = validate_configuration(
            configuration.configuration_type, version.canonical_json
        )
        issues.extend(
            self._validate_resource_bindings(
                configuration.project_id,
                configuration.configuration_type,
                version.canonical_json,
            )
        )
        version.validation_status = (
            "INVALID" if any(i["severity"] == "ERROR" for i in issues) else "VALID"
        )
        version.validation_summary = {"issues": issues}
        if version.validation_status == "VALID":
            self._clear_projection(version.id)
            self._project(
                configuration.configuration_type, version, version.canonical_json
            )
        return issues

    def publish(
        self,
        configuration: m.Configuration,
        version: m.ConfigurationVersion,
        actor_user_id: str,
    ) -> None:
        if version.status != "DRAFT":
            raise ConflictError("Only DRAFT configuration versions can be published")
        if version.validation_status != "VALID":
            raise ValidationError(
                [
                    _issue(
                        "configuration_invalid",
                        "Only valid configurations can be published",
                    )
                ]
            )
        version.status = "PUBLISHED"
        version.published_by = actor_user_id
        version.published_at = m.utcnow()
        add_audit(
            self.session,
            project_id=configuration.project_id,
            actor_user_id=actor_user_id,
            action="CONFIGURATION_VERSION_PUBLISH",
            resource_type="CONFIGURATION_VERSION",
            resource_id=version.id,
        )

    def _clear_projection(self, version_id: str) -> None:
        for model, column in (
            (
                m.FeatureSemanticsDatasetBinding,
                m.FeatureSemanticsDatasetBinding.configuration_version_id,
            ),
            (m.FeatureSemanticItem, m.FeatureSemanticItem.feature_semantics_version_id),
            (
                m.FeatureSemanticsProjection,
                m.FeatureSemanticsProjection.configuration_version_id,
            ),
            (m.CausalAssumption, m.CausalAssumption.causal_design_version_id),
            (
                m.CausalDesignProjection,
                m.CausalDesignProjection.configuration_version_id,
            ),
        ):
            self.session.query(model).filter(column == version_id).delete(
                synchronize_session=False
            )

    def _project(
        self,
        configuration_type: str,
        version: m.ConfigurationVersion,
        document: dict[str, Any],
    ) -> None:
        if configuration_type == "FEATURE_SEMANTICS":
            features = list(document.get("features", []))
            self.session.add(
                m.FeatureSemanticsProjection(
                    configuration_version_id=version.id,
                    default_unit_id=document.get("default_unit_id"),
                    feature_count=len(features),
                )
            )
            dataset_version_id = document.get("dataset_version_id")
            if dataset_version_id:
                binding = self.session.get(
                    m.AnalysisDatasetBinding, dataset_version_id
                )
                self.session.add(
                    m.FeatureSemanticsDatasetBinding(
                        configuration_version_id=version.id,
                        dataset_version_id=dataset_version_id,
                        dataset_table_version_id=binding.primary_table_version_id,
                        dataset_schema_hash_snapshot=binding.schema_hash_snapshot,
                        binding_status="VALID",
                        validation_summary_json={"issues": []},
                        validated_at=m.utcnow(),
                    )
                )
                dataset_columns = {
                    column.name: column.id
                    for column in self.session.scalars(
                        select(m.DatasetColumn).where(
                            m.DatasetColumn.dataset_table_version_id
                            == binding.primary_table_version_id
                        )
                    ).all()
                }
            else:
                dataset_columns = {}
            for item in features:
                role = item["role"]
                self.session.add(
                    m.FeatureSemanticItem(
                        feature_semantics_version_id=version.id,
                        name=item["name"],
                        role=item["role"],
                        source_table=item["source_table"],
                        source_column=item.get("source_column"),
                        unit_id=item.get("unit_id")
                        or document.get("default_unit_id")
                        or "unknown",
                        aggregation=item.get("aggregation"),
                        transform=item.get("transform"),
                        dtype=item.get("dtype"),
                        dataset_column_id=dataset_columns.get(
                            item.get("source_column") or item["name"]
                        ),
                        categorical=bool(item.get("categorical", False)),
                        allowed_for_discovery=bool(
                            item.get(
                                "allowed_for_discovery",
                                role not in {"identifier", "excluded"},
                            )
                        ),
                        allowed_for_adjustment=bool(
                            item.get("allowed_for_adjustment", False)
                        ),
                        post_treatment=bool(item.get("post_treatment", False)),
                        time_metadata_json=item.get("time_metadata", {}),
                        description=item.get("description"),
                        metadata_json=item.get("metadata", {}),
                    )
                )
        elif configuration_type == "CAUSAL_DESIGN":
            design = document.get("causal_design", document)
            treatment = design["treatment"]
            outcome = design["outcome"]
            self.session.add(
                m.CausalDesignProjection(
                    configuration_version_id=version.id,
                    feature_semantics_version_id=design.get(
                        "feature_semantics_version_id"
                    ),
                    dataset_version_id=design.get("dataset_version_id"),
                    causal_graph_version_id=design.get("causal_graph_version_id"),
                    estimand=design["estimand"],
                    treatment_name=treatment["name"],
                    treatment_time=treatment.get("time"),
                    treatment_levels=treatment.get("levels", []),
                    outcome_name=outcome["name"],
                    outcome_window=outcome.get("window"),
                    unit=design["unit"],
                    time_zero=design.get("time_zero"),
                    adjustment_set_name=(
                        design.get("adjustment_set")
                        if isinstance(design.get("adjustment_set"), str)
                        else None
                    ),
                    target_population=design.get("target_population"),
                    adjustment_strategy=design.get("adjustment_strategy"),
                    adjustment_set_json=design.get("adjustment_set", [])
                    if isinstance(design.get("adjustment_set", []), list)
                    else [],
                    analyst_note=design.get("analyst_note"),
                )
            )
            for ordinal, assumption in enumerate(
                design.get("assumptions", []), start=1
            ):
                if isinstance(assumption, str):
                    assumption = {"code": assumption}
                self.session.add(
                    m.CausalAssumption(
                        causal_design_version_id=version.id,
                        assumption_code=assumption.get("code")
                        or assumption.get("assumption_code"),
                        statement=assumption.get("statement"),
                        declaration_status=assumption.get(
                            "declaration_status", "DECLARED"
                        ),
                        evidence=assumption.get("evidence"),
                        ordinal=ordinal,
                    )
                )

    def _validate_resource_bindings(
        self,
        project_id: str,
        configuration_type: str,
        document: dict[str, Any],
    ) -> list[dict[str, Any]]:
        issues: list[dict[str, Any]] = []
        if configuration_type == "FEATURE_SEMANTICS":
            dataset_version_id = document.get("dataset_version_id")
            if not dataset_version_id:
                return issues  # Legacy semantics remain valid without a Dataset binding.
            version = self.session.get(m.DatasetVersion, dataset_version_id)
            dataset = self.session.get(m.Dataset, version.dataset_id) if version else None
            binding = self.session.get(m.AnalysisDatasetBinding, dataset_version_id)
            if (
                not version
                or not dataset
                or dataset.project_id != project_id
                or not binding
                or binding.readiness_status != "READY"
            ):
                return [
                    _issue(
                        "analysis_dataset_binding_invalid",
                        "Feature semantics requires a READY analysis Dataset binding",
                    )
                ]
            allowed_columns = {
                column.name
                for column, policy in self.session.execute(
                    select(m.DatasetColumn, m.DatasetColumnPolicy)
                    .join(
                        m.DatasetColumnPolicy,
                        m.DatasetColumnPolicy.dataset_column_id == m.DatasetColumn.id,
                    )
                    .where(
                        m.DatasetColumn.dataset_table_version_id
                        == binding.primary_table_version_id,
                        m.DatasetColumnPolicy.analysis_allowed.is_(True),
                    )
                ).all()
            }
            for ordinal, feature in enumerate(document.get("features", [])):
                source = feature.get("source_column") or feature.get("name")
                if source not in allowed_columns:
                    issues.append(
                        _issue(
                            "semantic_source_column_invalid",
                            f"Column is missing or not allowed for analysis: {source}",
                            f"features[{ordinal}]",
                        )
                    )
        elif configuration_type == "CAUSAL_DESIGN":
            design = document.get("causal_design", document)
            semantics_id = design.get("feature_semantics_version_id")
            dataset_id = design.get("dataset_version_id")
            graph_id = design.get("causal_graph_version_id")
            if any((semantics_id, dataset_id, graph_id)) and not all(
                (semantics_id, dataset_id, graph_id)
            ):
                issues.append(
                    _issue(
                        "causal_design_lineage_incomplete",
                        "Dataset, Feature Semantics, and Saved Graph must be specified together",
                    )
                )
            if all((semantics_id, dataset_id, graph_id)):
                graph = self.session.get(m.CausalGraphVersion, graph_id)
                binding = self.session.get(m.FeatureSemanticsDatasetBinding, semantics_id)
                if (
                    not graph
                    or graph.status != "PUBLISHED"
                    or graph.dataset_version_id != dataset_id
                    or graph.feature_semantics_version_id != semantics_id
                    or not binding
                    or binding.dataset_version_id != dataset_id
                ):
                    issues.append(
                        _issue(
                            "causal_design_lineage_mismatch",
                            "Causal Design inputs do not refer to the same published analysis lineage",
                        )
                    )
                items = {
                    item.name: item
                    for item in self.session.scalars(
                        select(m.FeatureSemanticItem).where(
                            m.FeatureSemanticItem.feature_semantics_version_id
                            == semantics_id
                        )
                    ).all()
                }
                treatment = design.get("treatment", {})
                outcome = design.get("outcome", {})
                treatment_name = (
                    treatment.get("name") if isinstance(treatment, dict) else treatment
                )
                outcome_name = outcome.get("name") if isinstance(outcome, dict) else outcome
                if items.get(treatment_name) is None or items[treatment_name].role != "treatment":
                    issues.append(
                        _issue(
                            "causal_design_treatment_invalid",
                            "Causal Design treatment must have the treatment role",
                        )
                    )
                if items.get(outcome_name) is None or items[outcome_name].role != "outcome":
                    issues.append(
                        _issue(
                            "causal_design_outcome_invalid",
                            "Causal Design outcome must have the outcome role",
                        )
                    )
                for name in design.get("adjustment_set", []):
                    item = items.get(name)
                    if (
                        not item
                        or item.role != "covariate"
                        or not item.allowed_for_adjustment
                        or item.post_treatment
                    ):
                        issues.append(
                            _issue(
                                "bad_control",
                                f"Variable is not an allowed pre-treatment covariate: {name}",
                            )
                        )
                node_names = set(
                    self.session.scalars(
                        select(m.CausalGraphNode.name).where(
                            m.CausalGraphNode.causal_graph_version_id == graph_id
                        )
                    ).all()
                )
                if treatment_name not in node_names or outcome_name not in node_names:
                    issues.append(
                        _issue(
                            "causal_design_graph_nodes_missing",
                            "Saved Graph must contain the treatment and outcome nodes",
                        )
                    )
        return issues


class ExecutionService:
    def __init__(self, session: MetadataRepository) -> None:
        self.session = session

    def create(
        self,
        *,
        request_document: dict[str, Any],
        actor_user_id: str,
        idempotency_key: str | None,
    ) -> tuple[m.Execution, bool]:
        project_id = request_document["project_id"]
        request_digest = canonical_hash(request_document)
        if idempotency_key:
            existing = self.session.scalar(
                select(m.Execution).where(
                    m.Execution.project_id == project_id,
                    m.Execution.idempotency_key == idempotency_key,
                )
            )
            if existing:
                if existing.request_hash != request_digest:
                    raise ConflictError(
                        "Idempotency-Key was already used with a different request"
                    )
                return existing, True
        stages, pipeline_version = self._resolve_stages(request_document)
        for stage in stages:
            stage["input_mode"] = stage.get("input_mode") or "CONFIGURED_FEATURE_BUILD"
        issues = self._validate_stages(
            project_id, stages, request_document["execution_mode"]
        )
        plan = {
            "schema_version": "2",
            "execution_id": None,
            "execution_mode": request_document["execution_mode"],
            "random_seed": request_document.get("random_seed"),
            "stages": [self._plan_stage(stage) for stage in stages],
            "validation_checks": [
                "resource_project_boundary",
                "published_configuration",
                "stage_dependency_acyclic",
                "feature_semantics_consistency",
                "causal_design_consistency",
                "adjustment_set_validity",
            ],
        }
        mode = request_document["execution_mode"]
        terminal = mode in {"DRY_RUN", "VALIDATE_ONLY"}
        status = (
            "FAILED"
            if terminal and any(i["severity"] == "ERROR" for i in issues)
            else ("SUCCEEDED" if terminal else "QUEUED")
        )
        mlflow_tracking_status = "NOT_REQUIRED" if terminal else "PENDING"
        run = m.Execution(
            project_id=project_id,
            experiment_id=request_document.get("experiment_id"),
            pipeline_definition_version_id=pipeline_version,
            execution_kind=request_document["execution_kind"],
            execution_mode=mode,
            status=status,
            submitted_by=actor_user_id,
            queued_at=None if terminal else m.utcnow(),
            finished_at=m.utcnow() if terminal else None,
            idempotency_key=idempotency_key,
            request_hash=request_digest,
            random_seed=request_document.get("random_seed"),
            priority=request_document.get("priority", 0),
            metadata_json=request_document.get("metadata", {}),
            mlflow_tracking_status=mlflow_tracking_status,
        )
        self.session.add(run)
        self.session.flush()
        plan["execution_id"] = run.id
        self.session.add(
            m.ExecutionPlanRecord(
                execution_id=run.id,
                canonical_json=plan,
                plan_hash=canonical_hash(plan),
            )
        )
        stage_records: dict[str, m.StageExecution] = {}
        for ordinal, stage in enumerate(stages, start=1):
            if not stage.get("enabled", True):
                continue
            stage_record = m.StageExecution(
                execution_id=run.id,
                stage_key=stage["stage_key"],
                stage_type=stage["stage_type"],
                analysis_mode=stage.get("analysis_mode"),
                input_mode=stage["input_mode"],
                ordinal=ordinal,
                runner_name=stage.get("runner_name") or stage["stage_type"].lower(),
                status=status if terminal else "QUEUED",
            )
            self.session.add(stage_record)
            self.session.flush()
            stage_records[stage["stage_key"]] = stage_record
            self._add_inputs(stage_record, stage)
        for stage in stages:
            if stage["stage_key"] not in stage_records:
                continue
            for dependency in stage.get("depends_on", []):
                self.session.add(
                    m.StageExecutionDependency(
                        stage_execution_id=stage_records[stage["stage_key"]].id,
                        depends_on_stage_execution_id=stage_records[dependency].id,
                    )
                )
        validation = m.ValidationExecution(
            execution_id=run.id,
            validator_name="web-plan-validator",
            validator_version="1",
            status="INVALID"
            if any(i["severity"] == "ERROR" for i in issues)
            else "VALID",
        )
        self.session.add(validation)
        self.session.flush()
        for ordinal, issue in enumerate(issues, start=1):
            self.session.add(
                m.ValidationIssueRecord(
                    validation_execution_id=validation.id, ordinal=ordinal, **issue
                )
            )
        self.add_event(
            run.id, "EXECUTION_CREATED", {"status": run.status, "execution_mode": mode}
        )
        if not terminal:
            self.session.add(
                m.OutboxEvent(
                    aggregate_type="EXECUTION",
                    aggregate_id=run.id,
                    event_type="EXECUTE_EXECUTION",
                    payload_json={"execution_id": run.id},
                )
            )
        add_audit(
            self.session,
            project_id=project_id,
            actor_user_id=actor_user_id,
            action="EXECUTION_CREATE",
            resource_type="EXECUTION",
            resource_id=run.id,
            after={"execution_mode": mode, "status": status},
        )
        return run, False

    def _plan_stage(self, stage: dict[str, Any]) -> dict[str, Any]:
        resolved = dict(stage)
        resolved["input_mode"] = stage.get("input_mode") or "CONFIGURED_FEATURE_BUILD"
        resolved["resolved_inputs"] = {
            "datasets": {
                name: {
                    "dataset_version_id": identifier,
                    "content_hash": version.content_hash if version else None,
                    "schema_hash": version.schema_hash if version else None,
                }
                for name, identifier in stage.get("dataset_inputs", {}).items()
                for version in (self.session.get(m.DatasetVersion, identifier),)
            },
            "configurations": {
                name: {
                    "configuration_version_id": identifier,
                    "content_hash": version.content_hash if version else None,
                }
                for name, identifier in stage.get("configuration_inputs", {}).items()
                for version in (self.session.get(m.ConfigurationVersion, identifier),)
            },
            "saved_graphs": {
                name: {
                    "causal_graph_version_id": identifier,
                    "content_hash": version.content_hash if version else None,
                }
                for name, identifier in stage.get("graph_inputs", {}).items()
                for version in (self.session.get(m.CausalGraphVersion, identifier),)
            },
        }
        return resolved

    def retry(self, run: m.Execution, actor_user_id: str) -> m.Execution:
        if run.status not in {"FAILED", "CANCELLED"}:
            raise ConflictError("Only FAILED or CANCELLED runs can be retried")
        stages = self.session.scalars(
            select(m.StageExecution)
            .where(m.StageExecution.execution_id == run.id)
            .order_by(m.StageExecution.ordinal)
        ).all()
        first_retry_ordinal = min(
            (stage.ordinal for stage in stages if stage.status != "SUCCEEDED"),
            default=None,
        )
        if first_retry_ordinal is None:
            raise ConflictError("Run has no failed or cancelled stage to retry")
        for stage in stages:
            if stage.ordinal >= first_retry_ordinal:
                stage.status = "QUEUED"
                stage.selected_attempt_id = None
                stage.started_at = None
                stage.finished_at = None
                stage.error_code = None
                stage.error_summary = None
        run.status = "QUEUED"
        run.queued_at = m.utcnow()
        run.started_at = None
        run.finished_at = None
        run.cancel_requested_at = None
        run.error_code = None
        run.error_summary = None
        self.add_event(
            run.id,
            "EXECUTION_RETRY_QUEUED",
            {"first_retry_ordinal": first_retry_ordinal, "requested_by": actor_user_id},
        )
        self.session.add(
            m.OutboxEvent(
                aggregate_type="EXECUTION",
                aggregate_id=run.id,
                event_type="EXECUTE_EXECUTION",
                payload_json={"execution_id": run.id},
            )
        )
        return run

    def add_event(
        self,
        execution_id: str,
        event_type: str,
        payload: dict[str, Any],
        *,
        stage_execution_id: str | None = None,
        attempt_id: str | None = None,
    ) -> None:
        sequence = (
            self.session.scalar(
                select(func.max(m.ExecutionEvent.sequence_number)).where(
                    m.ExecutionEvent.execution_id == execution_id
                )
            )
            or 0
        ) + 1
        self.session.add(
            m.ExecutionEvent(
                execution_id=execution_id,
                stage_execution_id=stage_execution_id,
                stage_attempt_id=attempt_id,
                sequence_number=sequence,
                event_type=event_type,
                payload_json=payload,
            )
        )

    def _resolve_stages(
        self, request: dict[str, Any]
    ) -> tuple[list[dict[str, Any]], str | None]:
        if request.get("stages") is not None:
            return request["stages"], None
        version = self.session.get(
            m.PipelineDefinitionVersion, request["pipeline_definition_version_id"]
        )
        if version is None:
            raise ResourceNotFoundError("Pipeline definition version not found")
        definition = self.session.get(
            m.PipelineDefinition, version.pipeline_definition_id
        )
        if definition.project_id != request["project_id"]:
            raise ResourceNotFoundError("Pipeline definition version not found")
        if request["execution_mode"] == "RUN" and version.status != "PUBLISHED":
            raise ValidationError(
                [_issue("pipeline_not_published", "RUN requires a published pipeline")]
            )
        return list(version.canonical_json["stages"]), version.id

    def _validate_stages(
        self, project_id: str, stages: list[dict[str, Any]], mode: str
    ) -> list[dict[str, Any]]:
        issues: list[dict[str, Any]] = []
        keys = [stage["stage_key"] for stage in stages]
        if len(set(keys)) != len(keys):
            issues.append(_issue("duplicate_stage_key", "Stage keys must be unique"))
        for stage in stages:
            unknown = set(stage.get("depends_on", [])) - set(keys)
            if unknown:
                issues.append(
                    _issue(
                        "unknown_stage_dependency",
                        f"Unknown dependencies: {sorted(unknown)}",
                    )
                )
            if (
                stage["stage_type"] == "INFERENCE"
                and stage.get("analysis_mode") == "EDGE_WEIGHT"
            ):
                if (
                    not stage.get("artifact_inputs")
                    and not stage.get("graph_inputs")
                    and not stage.get("depends_on")
                ):
                    issues.append(
                        _issue(
                            "edge_artifact_required",
                            "EDGE_WEIGHT requires a discovery artifact or dependency",
                        )
                    )
            config_versions: dict[str, m.ConfigurationVersion] = {}
            for name, version_id in stage.get("configuration_inputs", {}).items():
                version = self.session.get(m.ConfigurationVersion, version_id)
                configuration = (
                    self.session.get(m.Configuration, version.configuration_id)
                    if version
                    else None
                )
                if (
                    not version
                    or not configuration
                    or configuration.project_id != project_id
                ):
                    issues.append(
                        _issue(
                            "configuration_not_found",
                            f"Configuration input not found: {name}",
                        )
                    )
                elif mode == "RUN" and version.status != "PUBLISHED":
                    issues.append(
                        _issue(
                            "configuration_not_published",
                            f"RUN requires published configuration: {name}",
                        )
                    )
                else:
                    config_versions[name] = version
                    expected_type = _expected_configuration_type(stage, name)
                    if (
                        expected_type
                        and configuration.configuration_type != expected_type
                    ):
                        issues.append(
                            _issue(
                                "configuration_type_mismatch",
                                f"{name} requires {expected_type}, got {configuration.configuration_type}",
                            )
                        )
            for name, version_id in stage.get("dataset_inputs", {}).items():
                version = self.session.get(m.DatasetVersion, version_id)
                dataset = (
                    self.session.get(m.Dataset, version.dataset_id) if version else None
                )
                if (
                    not version
                    or not dataset
                    or dataset.project_id != project_id
                    or version.status != "READY"
                ):
                    issues.append(
                        _issue(
                            "dataset_not_ready", f"Dataset input is not READY: {name}"
                        )
                    )
            for name, artifact_id in stage.get("artifact_inputs", {}).items():
                artifact = self.session.get(m.Artifact, artifact_id)
                if (
                    not artifact
                    or artifact.project_id != project_id
                    or artifact.status != "AVAILABLE"
                ):
                    issues.append(
                        _issue(
                            "artifact_not_available",
                            f"Artifact input is not AVAILABLE: {name}",
                        )
                    )
            input_mode = stage.get("input_mode") or "CONFIGURED_FEATURE_BUILD"
            if input_mode == "ANALYSIS_READY":
                issues.extend(
                    self._validate_analysis_ready_inputs(
                        project_id, stage, config_versions
                    )
                )
            for name, graph_version_id in stage.get("graph_inputs", {}).items():
                graph_version = self.session.get(
                    m.CausalGraphVersion, graph_version_id
                )
                graph = (
                    self.session.get(m.CausalGraph, graph_version.causal_graph_id)
                    if graph_version
                    else None
                )
                if (
                    not graph_version
                    or not graph
                    or graph.project_id != project_id
                    or graph_version.status != "PUBLISHED"
                ):
                    issues.append(
                        _issue(
                            "causal_graph_not_published",
                            f"Saved graph input is not PUBLISHED: {name}",
                        )
                    )
            if stage.get("analysis_mode") == "TREATMENT_EFFECT":
                issues.extend(self._validate_treatment_effect(stage, config_versions))
        if not _acyclic(stages):
            issues.append(
                _issue("pipeline_cycle", "Pipeline dependencies must be acyclic")
            )
        return issues

    def _validate_analysis_ready_inputs(
        self,
        project_id: str,
        stage: dict[str, Any],
        versions: dict[str, m.ConfigurationVersion],
    ) -> list[dict[str, Any]]:
        issues: list[dict[str, Any]] = []
        dataset_ids = list(stage.get("dataset_inputs", {}).values())
        semantics = versions.get("feature_semantics")
        if len(dataset_ids) != 1:
            issues.append(
                _issue(
                    "analysis_dataset_count_invalid",
                    "ANALYSIS_READY requires exactly one Dataset Version",
                )
            )
            return issues
        binding = self.session.get(m.AnalysisDatasetBinding, dataset_ids[0])
        semantics_binding = (
            self.session.get(m.FeatureSemanticsDatasetBinding, semantics.id)
            if semantics
            else None
        )
        if not binding or binding.readiness_status != "READY":
            issues.append(
                _issue(
                    "analysis_dataset_not_ready",
                    "ANALYSIS_READY requires a READY analysis Dataset binding",
                )
            )
        if (
            not semantics
            or not semantics_binding
            or semantics_binding.binding_status != "VALID"
            or semantics_binding.dataset_version_id != dataset_ids[0]
        ):
            issues.append(
                _issue(
                    "feature_semantics_binding_invalid",
                    "ANALYSIS_READY requires published Feature Semantics bound to the Dataset Version",
                )
            )
        graph_ids = list(stage.get("graph_inputs", {}).values())
        if stage.get("stage_type") == "INFERENCE" and len(graph_ids) != 1:
            issues.append(
                _issue(
                    "causal_graph_input_required",
                    "ANALYSIS_READY inference requires exactly one Saved Graph Version",
                )
            )
        if graph_ids and semantics:
            graph = self.session.get(m.CausalGraphVersion, graph_ids[0])
            if graph and (
                graph.dataset_version_id != dataset_ids[0]
                or graph.feature_semantics_version_id != semantics.id
            ):
                issues.append(
                    _issue(
                        "causal_graph_lineage_mismatch",
                        "Saved Graph does not match the Dataset and Feature Semantics inputs",
                    )
                )
        return issues

    def _validate_treatment_effect(
        self,
        stage: dict[str, Any],
        versions: dict[str, m.ConfigurationVersion],
    ) -> list[dict[str, Any]]:
        issues: list[dict[str, Any]] = []
        semantics = versions.get("feature_semantics")
        design_version = versions.get("causal_design")
        if not semantics or not design_version:
            return [
                _issue(
                    "treatment_effect_inputs_missing",
                    "Treatment effect requires feature_semantics and causal_design",
                )
            ]
        design = self.session.get(m.CausalDesignProjection, design_version.id)
        items = self.session.scalars(
            select(m.FeatureSemanticItem).where(
                m.FeatureSemanticItem.feature_semantics_version_id == semantics.id
            )
        ).all()
        by_name = {item.name: item for item in items}
        if not design:
            return [
                _issue(
                    "causal_design_projection_missing",
                    "Causal design is not valid/projected",
                )
            ]
        graph_id = next(iter(stage.get("graph_inputs", {}).values()), None)
        dataset_id = next(iter(stage.get("dataset_inputs", {}).values()), None)
        if stage.get("input_mode") == "ANALYSIS_READY" and (
            design.feature_semantics_version_id != semantics.id
            or design.dataset_version_id != dataset_id
            or design.causal_graph_version_id != graph_id
        ):
            issues.append(
                _issue(
                    "causal_design_run_mismatch",
                    "Run inputs must match the Dataset, Semantics, and Saved Graph declared by Causal Design",
                )
            )
        treatment = by_name.get(design.treatment_name)
        outcome = by_name.get(design.outcome_name)
        if not treatment or treatment.role != "treatment":
            issues.append(
                _issue(
                    "treatment_semantics_invalid",
                    f"Invalid treatment semantics: {design.treatment_name}",
                )
            )
        if not outcome or outcome.role != "outcome":
            issues.append(
                _issue(
                    "outcome_semantics_invalid",
                    f"Invalid outcome semantics: {design.outcome_name}",
                )
            )
        configured = stage.get("parameters", {})
        if configured.get("estimand") and configured["estimand"] != design.estimand:
            issues.append(
                _issue("estimand_mismatch", "Run estimand differs from causal design")
            )
        for variable in configured.get("covariates", []):
            item = by_name.get(variable)
            if (
                not item
                or item.role != "covariate"
                or not item.allowed_for_adjustment
                or item.post_treatment
            ):
                issues.append(
                    _issue(
                        "bad_control",
                        f"Variable is not an allowed pre-treatment covariate: {variable}",
                    )
                )
        return issues

    def _add_inputs(self, stage_record: m.StageExecution, stage: dict[str, Any]) -> None:
        for name, version_id in stage.get("dataset_inputs", {}).items():
            self.session.add(
                m.StageExecutionDatasetInput(
                    stage_execution_id=stage_record.id,
                    input_name=name,
                    dataset_version_id=version_id,
                )
            )
        for name, version_id in stage.get("configuration_inputs", {}).items():
            version = self.session.get(m.ConfigurationVersion, version_id)
            if version:
                self.session.add(
                    m.StageExecutionConfigInput(
                        stage_execution_id=stage_record.id,
                        input_name=name,
                        configuration_version_id=version_id,
                        content_hash_snapshot=version.content_hash,
                    )
                )
        for name, artifact_id in stage.get("artifact_inputs", {}).items():
            self.session.add(
                m.StageExecutionArtifactInput(
                    stage_execution_id=stage_record.id,
                    input_name=name,
                    artifact_id=artifact_id,
                )
            )
        for name, graph_version_id in stage.get("graph_inputs", {}).items():
            graph = self.session.get(m.CausalGraphVersion, graph_version_id)
            if graph:
                self.session.add(
                    m.StageExecutionGraphInput(
                        stage_execution_id=stage_record.id,
                        input_name=name,
                        causal_graph_version_id=graph.id,
                        content_hash_snapshot=graph.content_hash,
                        source="API_OVERRIDE",
                    )
                )
        self._add_input_preparation(stage_record, stage)
        for name, value in stage.get("parameters", {}).items():
            self.session.add(
                m.StageExecutionParameter(
                    stage_execution_id=stage_record.id,
                    parameter_name=name,
                    value_json=value,
                    source="API_OVERRIDE",
                )
            )

    def _add_input_preparation(
        self, stage_record: m.StageExecution, stage: dict[str, Any]
    ) -> None:
        dataset_id = next(iter(stage.get("dataset_inputs", {}).values()), None)
        if not dataset_id:
            return
        version = self.session.get(m.DatasetVersion, dataset_id)
        configs = stage.get("configuration_inputs", {})
        semantics_id = configs.get("feature_semantics")
        feature_id = configs.get("feature_config")
        table_id = None
        if stage_record.input_mode == "ANALYSIS_READY":
            binding = self.session.get(m.AnalysisDatasetBinding, dataset_id)
            table_id = binding.primary_table_version_id if binding else None
        parameters = stage.get("parameters", {})
        self.session.add(
            m.StageExecutionInputPreparation(
                stage_execution_id=stage_record.id,
                input_mode=stage_record.input_mode,
                input_dataset_version_id=dataset_id,
                input_table_version_id=table_id,
                input_schema_hash=version.schema_hash or "",
                feature_semantics_version_id=semantics_id,
                requested_columns_json=parameters.get(
                    "selected_columns", parameters.get("columns", [])
                ),
                conditioning_spec_json=parameters.get("conditioning", {}),
                configured_feature_version_id=feature_id,
            )
        )


def validate_configuration(
    configuration_type: str, document: dict[str, Any]
) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    if configuration_type == "FEATURE_SEMANTICS":
        features = document.get("features")
        if not isinstance(features, list) or not features:
            return [
                _issue(
                    "features_required",
                    "Feature semantics requires a non-empty features list",
                )
            ]
        names: set[str] = set()
        roles = {
            "identifier",
            "treatment",
            "outcome",
            "covariate",
            "mediator",
            "collider",
            "post_treatment",
            "excluded",
        }
        for ordinal, feature in enumerate(features):
            location = f"features[{ordinal}]"
            missing = {"name", "role", "source_table"} - set(feature)
            if missing:
                issues.append(
                    _issue(
                        "feature_fields_missing",
                        f"Missing fields: {sorted(missing)}",
                        location,
                    )
                )
                continue
            if feature["name"] in names:
                issues.append(
                    _issue(
                        "duplicate_feature",
                        f"Duplicate feature: {feature['name']}",
                        location,
                    )
                )
            names.add(feature["name"])
            if feature["role"] not in roles:
                issues.append(
                    _issue(
                        "feature_role_invalid",
                        f"Unsupported feature role: {feature['role']}",
                        location,
                    )
                )
            forbidden = feature["role"] in {
                "treatment",
                "outcome",
                "mediator",
                "collider",
                "post_treatment",
            }
            if forbidden and feature.get("allowed_for_adjustment", False):
                issues.append(
                    _issue(
                        "adjustment_forbidden_role",
                        f"{feature['name']} cannot be used for adjustment",
                        location,
                    )
                )
            if feature.get("post_treatment") and feature.get(
                "allowed_for_adjustment", False
            ):
                issues.append(
                    _issue(
                        "adjustment_post_treatment",
                        f"{feature['name']} is post-treatment",
                        location,
                    )
                )
        treatments = [
            feature.get("name")
            for feature in features
            if feature.get("role") == "treatment"
        ]
        outcomes = [
            feature.get("name")
            for feature in features
            if feature.get("role") == "outcome"
        ]
        if set(treatments) & set(outcomes):
            issues.append(
                _issue(
                    "treatment_outcome_same",
                    "Treatment and outcome must not use the same feature",
                )
            )
    elif configuration_type == "CAUSAL_DESIGN":
        design = document.get("causal_design", document)
        missing = {"estimand", "treatment", "outcome", "unit"} - set(design)
        if missing:
            issues.append(
                _issue(
                    "causal_design_fields_missing", f"Missing fields: {sorted(missing)}"
                )
            )
        elif design["estimand"] not in {"ATE", "ATT"}:
            issues.append(_issue("estimand_invalid", "MVP estimand must be ATE or ATT"))
        if (
            isinstance(design.get("treatment"), dict)
            and "name" not in design["treatment"]
        ):
            issues.append(
                _issue("treatment_name_required", "Treatment name is required")
            )
        if isinstance(design.get("outcome"), dict) and "name" not in design["outcome"]:
            issues.append(_issue("outcome_name_required", "Outcome name is required"))
    elif not document:
        issues.append(_issue("configuration_empty", "Configuration cannot be empty"))
    return issues


def _issue(code: str, message: str, location: str | None = None) -> dict[str, Any]:
    return {
        "severity": "ERROR",
        "code": code,
        "message": message,
        "location": location,
        "payload_json": {},
    }


def _acyclic(stages: list[dict[str, Any]]) -> bool:
    graph = {stage["stage_key"]: set(stage.get("depends_on", [])) for stage in stages}
    temporary: set[str] = set()
    permanent: set[str] = set()

    def visit(node: str) -> bool:
        if node in permanent:
            return True
        if node in temporary:
            return False
        temporary.add(node)
        if any(not visit(parent) for parent in graph.get(node, set())):
            return False
        temporary.remove(node)
        permanent.add(node)
        return True

    return all(visit(node) for node in graph)


def _expected_configuration_type(stage: dict[str, Any], name: str) -> str | None:
    if name == "feature_semantics":
        return "FEATURE_SEMANTICS"
    if name == "causal_design":
        return "CAUSAL_DESIGN"
    if name in {"analysis_config", "config"}:
        return (
            "DISCOVERY_ANALYSIS"
            if stage.get("stage_type") == "DISCOVERY"
            else "INFERENCE_ANALYSIS"
            if stage.get("stage_type") == "INFERENCE"
            else None
        )
    if name == "feature_config":
        return (
            "DISCOVERY_FEATURE"
            if stage.get("stage_type") == "DISCOVERY"
            else "INFERENCE_FEATURE"
            if stage.get("stage_type") == "INFERENCE"
            else None
        )
    return None


def _hash_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


__all__ = [
    "ConflictError",
    "ResourceNotFoundError",
    "ExecutionService",
    "ValidationError",
    "add_audit",
    "canonical_hash",
    "validate_configuration",
]
