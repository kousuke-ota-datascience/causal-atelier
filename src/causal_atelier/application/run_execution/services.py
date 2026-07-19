"""Run execution use cases and shared control-plane policies."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import yaml
from sqlalchemy import func, select

from causal_atelier.application.ports import ArtifactStore, DataQuery, MetadataRepository
from causal_atelier.domain import metadata as m


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
        version.schema_hash = canonical_hash(
            [{"name": raw["logical_name"]} for raw in tables]
        )
        version.content_hash = canonical_hash(table_hashes)
        version.status = "READY"
        version.ready_at = m.utcnow()
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
            for item in features:
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
                        allowed_for_adjustment=bool(
                            item.get("allowed_for_adjustment", False)
                        ),
                        post_treatment=bool(item.get("post_treatment", False)),
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
                    estimand=design["estimand"],
                    treatment_name=treatment["name"],
                    treatment_time=treatment.get("time"),
                    treatment_levels=treatment.get("levels", []),
                    outcome_name=outcome["name"],
                    outcome_window=outcome.get("window"),
                    unit=design["unit"],
                    time_zero=design.get("time_zero"),
                    adjustment_set_name=design.get("adjustment_set"),
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


class RunService:
    def __init__(self, session: MetadataRepository) -> None:
        self.session = session

    def create(
        self,
        *,
        request_document: dict[str, Any],
        actor_user_id: str,
        idempotency_key: str | None,
    ) -> tuple[m.Run, bool]:
        project_id = request_document["project_id"]
        request_digest = canonical_hash(request_document)
        if idempotency_key:
            existing = self.session.scalar(
                select(m.Run).where(
                    m.Run.project_id == project_id,
                    m.Run.idempotency_key == idempotency_key,
                )
            )
            if existing:
                if existing.request_hash != request_digest:
                    raise ConflictError(
                        "Idempotency-Key was already used with a different request"
                    )
                return existing, True
        stages, pipeline_version = self._resolve_stages(request_document)
        issues = self._validate_stages(
            project_id, stages, request_document["execution_mode"]
        )
        plan = {
            "schema_version": "2",
            "run_id": None,
            "execution_mode": request_document["execution_mode"],
            "random_seed": request_document.get("random_seed"),
            "stages": stages,
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
        run = m.Run(
            project_id=project_id,
            experiment_id=request_document.get("experiment_id"),
            pipeline_definition_version_id=pipeline_version,
            run_kind=request_document["run_kind"],
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
        )
        self.session.add(run)
        self.session.flush()
        plan["run_id"] = run.id
        self.session.add(
            m.ExecutionPlanRecord(
                run_id=run.id,
                canonical_json=plan,
                plan_hash=canonical_hash(plan),
            )
        )
        stage_records: dict[str, m.StageRun] = {}
        for ordinal, stage in enumerate(stages, start=1):
            if not stage.get("enabled", True):
                continue
            stage_record = m.StageRun(
                run_id=run.id,
                stage_key=stage["stage_key"],
                stage_type=stage["stage_type"],
                analysis_mode=stage.get("analysis_mode"),
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
                    m.StageRunDependency(
                        stage_run_id=stage_records[stage["stage_key"]].id,
                        depends_on_stage_run_id=stage_records[dependency].id,
                    )
                )
        validation = m.ValidationRun(
            run_id=run.id,
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
                    validation_run_id=validation.id, ordinal=ordinal, **issue
                )
            )
        self.add_event(
            run.id, "RUN_CREATED", {"status": run.status, "execution_mode": mode}
        )
        if not terminal:
            self.session.add(
                m.OutboxEvent(
                    aggregate_type="RUN",
                    aggregate_id=run.id,
                    event_type="EXECUTE_RUN",
                    payload_json={"run_id": run.id},
                )
            )
        add_audit(
            self.session,
            project_id=project_id,
            actor_user_id=actor_user_id,
            action="RUN_CREATE",
            resource_type="RUN",
            resource_id=run.id,
            after={"execution_mode": mode, "status": status},
        )
        return run, False

    def retry(self, run: m.Run, actor_user_id: str) -> m.Run:
        if run.status not in {"FAILED", "CANCELLED"}:
            raise ConflictError("Only FAILED or CANCELLED runs can be retried")
        stages = self.session.scalars(
            select(m.StageRun)
            .where(m.StageRun.run_id == run.id)
            .order_by(m.StageRun.ordinal)
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
            "RUN_RETRY_QUEUED",
            {"first_retry_ordinal": first_retry_ordinal, "requested_by": actor_user_id},
        )
        self.session.add(
            m.OutboxEvent(
                aggregate_type="RUN",
                aggregate_id=run.id,
                event_type="EXECUTE_RUN",
                payload_json={"run_id": run.id},
            )
        )
        return run

    def add_event(
        self,
        run_id: str,
        event_type: str,
        payload: dict[str, Any],
        *,
        stage_run_id: str | None = None,
        attempt_id: str | None = None,
    ) -> None:
        sequence = (
            self.session.scalar(
                select(func.max(m.RunEvent.sequence_number)).where(
                    m.RunEvent.run_id == run_id
                )
            )
            or 0
        ) + 1
        self.session.add(
            m.RunEvent(
                run_id=run_id,
                stage_run_id=stage_run_id,
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
                if not stage.get("artifact_inputs") and not stage.get("depends_on"):
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
            if stage.get("analysis_mode") == "TREATMENT_EFFECT":
                issues.extend(self._validate_treatment_effect(stage, config_versions))
        if not _acyclic(stages):
            issues.append(
                _issue("pipeline_cycle", "Pipeline dependencies must be acyclic")
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

    def _add_inputs(self, stage_record: m.StageRun, stage: dict[str, Any]) -> None:
        for name, version_id in stage.get("dataset_inputs", {}).items():
            self.session.add(
                m.StageRunDatasetInput(
                    stage_run_id=stage_record.id,
                    input_name=name,
                    dataset_version_id=version_id,
                )
            )
        for name, version_id in stage.get("configuration_inputs", {}).items():
            version = self.session.get(m.ConfigurationVersion, version_id)
            if version:
                self.session.add(
                    m.StageRunConfigInput(
                        stage_run_id=stage_record.id,
                        input_name=name,
                        configuration_version_id=version_id,
                        content_hash_snapshot=version.content_hash,
                    )
                )
        for name, artifact_id in stage.get("artifact_inputs", {}).items():
            self.session.add(
                m.StageRunArtifactInput(
                    stage_run_id=stage_record.id,
                    input_name=name,
                    artifact_id=artifact_id,
                )
            )
        for name, value in stage.get("parameters", {}).items():
            self.session.add(
                m.StageRunParameter(
                    stage_run_id=stage_record.id,
                    parameter_name=name,
                    value_json=value,
                    source="API_OVERRIDE",
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
            "treatment",
            "outcome",
            "covariate",
            "mediator",
            "collider",
            "post_treatment",
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


def _hash_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


__all__ = [
    "ConflictError",
    "ResourceNotFoundError",
    "RunService",
    "ValidationError",
    "add_audit",
    "canonical_hash",
    "validate_configuration",
]
