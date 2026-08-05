"""Configuration, experiment, and reusable pipeline definition endpoints."""

from __future__ import annotations

import yaml
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import Response
from sqlalchemy import func, select
from ariadne.application.control_plane import ControlPlaneService as Session

from ariadne.application.configuration_catalog import ConfigurationService
from ariadne.application.run_execution.services import (
    ConflictError,
    ValidationError,
    add_audit,
    canonical_hash,
)
from ariadne.domain import metadata as m
from ariadne.interfaces.api.dependencies import (
    RequestUser,
    get_current_user,
    get_session,
    require_project_role,
)
from ariadne.interfaces.api.schemas import (
    ConfigurationCreate,
    ConfigurationVersionCreate,
    ExperimentCreate,
    PipelineDefinitionCreate,
    PipelineDefinitionVersionCreate,
)

from .common import get_or_404, model_dict, project_for_configuration_version


router = APIRouter(tags=["configurations", "experiments", "pipelines"])


@router.post("/configurations", status_code=status.HTTP_201_CREATED)
def create_configuration(
    body: ConfigurationCreate,
    request: Request,
    session: Session = Depends(get_session),
    user: RequestUser = Depends(get_current_user),
) -> dict:
    require_project_role(session, user, body.project_id, "ANALYST")
    existing = session.scalar(
        select(m.Configuration).where(
            m.Configuration.project_id == body.project_id,
            m.Configuration.configuration_type == body.configuration_type,
            func.lower(m.Configuration.slug) == body.slug.lower(),
        )
    )
    if existing:
        raise HTTPException(
            status.HTTP_409_CONFLICT, "Configuration slug already exists for this type"
        )
    configuration = m.Configuration(**body.model_dump(), created_by=user.id)
    session.add(configuration)
    session.flush()
    add_audit(
        session,
        project_id=body.project_id,
        actor_user_id=user.id,
        action="CONFIGURATION_CREATE",
        resource_type="CONFIGURATION",
        resource_id=configuration.id,
        request_id=request.state.request_id,
        after=body.model_dump(),
    )
    return model_dict(configuration)


@router.get("/configurations")
def list_configurations(
    project_id: str,
    configuration_type: str | None = None,
    session: Session = Depends(get_session),
    user: RequestUser = Depends(get_current_user),
) -> list[dict]:
    require_project_role(session, user, project_id)
    query = select(m.Configuration).where(
        m.Configuration.project_id == project_id, m.Configuration.deleted_at.is_(None)
    )
    if configuration_type:
        query = query.where(m.Configuration.configuration_type == configuration_type)
    return [
        model_dict(item)
        for item in session.scalars(
            query.order_by(m.Configuration.created_at.desc())
        ).all()
    ]


@router.post(
    "/configurations/{configuration_id}/versions", status_code=status.HTTP_201_CREATED
)
def create_configuration_version(
    configuration_id: str,
    body: ConfigurationVersionCreate,
    session: Session = Depends(get_session),
    user: RequestUser = Depends(get_current_user),
) -> dict:
    configuration = get_or_404(session, m.Configuration, configuration_id)
    require_project_role(session, user, configuration.project_id, "ANALYST")
    try:
        version = ConfigurationService(session).create_version(
            configuration,
            actor_user_id=user.id,
            canonical_json=body.canonical_json,
            yaml_text=body.yaml_text,
            schema_version=body.schema_version,
        )
    except ConflictError as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, str(exc)) from exc
    except (yaml.YAMLError, ValidationError) as exc:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, str(exc)) from exc
    return model_dict(version, exclude={"original_text"})


@router.get("/configurations/{configuration_id}/versions")
def list_configuration_versions(
    configuration_id: str,
    version_status: str | None = None,
    session: Session = Depends(get_session),
    user: RequestUser = Depends(get_current_user),
) -> list[dict]:
    configuration = get_or_404(session, m.Configuration, configuration_id)
    require_project_role(session, user, configuration.project_id)
    query = select(m.ConfigurationVersion).where(
        m.ConfigurationVersion.configuration_id == configuration.id
    )
    if version_status:
        query = query.where(m.ConfigurationVersion.status == version_status)
    versions = session.scalars(
        query.order_by(m.ConfigurationVersion.version_number.desc())
    ).all()
    return [model_dict(item, exclude={"original_text"}) for item in versions]


@router.get("/configuration-versions/{version_id}")
def get_configuration_version(
    version_id: str,
    session: Session = Depends(get_session),
    user: RequestUser = Depends(get_current_user),
) -> dict:
    version = get_or_404(session, m.ConfigurationVersion, version_id)
    require_project_role(
        session, user, project_for_configuration_version(session, version)
    )
    return model_dict(version, exclude={"original_text"})


@router.get("/configuration-versions/{version_id}/export")
def export_configuration_version(
    version_id: str,
    session: Session = Depends(get_session),
    user: RequestUser = Depends(get_current_user),
) -> Response:
    version = get_or_404(session, m.ConfigurationVersion, version_id)
    require_project_role(
        session, user, project_for_configuration_version(session, version)
    )
    text = (
        version.original_text
        if version.original_format == "YAML" and version.original_text
        else yaml.safe_dump(version.canonical_json, sort_keys=False)
    )
    return Response(text, media_type="application/yaml")


@router.post("/configuration-versions/{version_id}/validate")
def validate_configuration_version(
    version_id: str,
    session: Session = Depends(get_session),
    user: RequestUser = Depends(get_current_user),
) -> dict:
    version = get_or_404(session, m.ConfigurationVersion, version_id)
    configuration = get_or_404(session, m.Configuration, version.configuration_id)
    require_project_role(session, user, configuration.project_id, "ANALYST")
    issues = ConfigurationService(session).validate(configuration, version)
    return {
        "version_id": version.id,
        "status": version.validation_status,
        "issues": issues,
    }


@router.post("/configuration-versions/{version_id}/publish")
def publish_configuration_version(
    version_id: str,
    session: Session = Depends(get_session),
    user: RequestUser = Depends(get_current_user),
) -> dict:
    version = get_or_404(session, m.ConfigurationVersion, version_id)
    configuration = get_or_404(session, m.Configuration, version.configuration_id)
    require_project_role(session, user, configuration.project_id, "ANALYST")
    try:
        ConfigurationService(session).publish(configuration, version, user.id)
    except ConflictError as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, str(exc)) from exc
    except ValidationError as exc:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, str(exc)) from exc
    return model_dict(version, exclude={"original_text"})


@router.post("/experiments", status_code=status.HTTP_201_CREATED)
def create_experiment(
    body: ExperimentCreate,
    request: Request,
    session: Session = Depends(get_session),
    user: RequestUser = Depends(get_current_user),
) -> dict:
    require_project_role(session, user, body.project_id, "ANALYST")
    existing = session.scalar(
        select(m.Experiment).where(
            m.Experiment.project_id == body.project_id,
            func.lower(m.Experiment.slug) == body.slug.lower(),
        )
    )
    if existing:
        raise HTTPException(status.HTTP_409_CONFLICT, "Experiment slug already exists")
    experiment = m.Experiment(**body.model_dump(), created_by=user.id)
    session.add(experiment)
    session.flush()
    add_audit(
        session,
        project_id=body.project_id,
        actor_user_id=user.id,
        action="EXPERIMENT_CREATE",
        resource_type="EXPERIMENT",
        resource_id=experiment.id,
        request_id=request.state.request_id,
    )
    return model_dict(experiment)


@router.post("/pipeline-definitions", status_code=status.HTTP_201_CREATED)
def create_pipeline_definition(
    body: PipelineDefinitionCreate,
    request: Request,
    session: Session = Depends(get_session),
    user: RequestUser = Depends(get_current_user),
) -> dict:
    require_project_role(session, user, body.project_id, "ANALYST")
    keys = {stage.stage_key for stage in body.stages}
    if len(keys) != len(body.stages):
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY, "Stage keys must be unique"
        )
    for stage in body.stages:
        if not set(stage.depends_on).issubset(keys):
            raise HTTPException(
                status.HTTP_422_UNPROCESSABLE_ENTITY,
                f"Unknown dependency in stage {stage.stage_key}",
            )
    definition = m.PipelineDefinition(
        project_id=body.project_id,
        slug=body.slug,
        name=body.name,
        description=body.description,
        created_by=user.id,
    )
    session.add(definition)
    session.flush()
    canonical = {
        "random_seed_default": body.random_seed_default,
        "fail_fast": body.fail_fast,
        "stages": [stage.model_dump() for stage in body.stages],
    }
    version = m.PipelineDefinitionVersion(
        pipeline_definition_id=definition.id,
        version_number=1,
        status="PUBLISHED" if body.publish else "DRAFT",
        random_seed_default=body.random_seed_default,
        fail_fast=body.fail_fast,
        canonical_json=canonical,
        content_hash=canonical_hash(canonical),
        created_by=user.id,
        published_at=m.utcnow() if body.publish else None,
    )
    session.add(version)
    session.flush()
    stage_records: dict[str, m.PipelineStageDefinition] = {}
    for ordinal, stage in enumerate(body.stages, start=1):
        record = m.PipelineStageDefinition(
            pipeline_definition_version_id=version.id,
            stage_key=stage.stage_key,
            stage_type=stage.stage_type,
            analysis_mode=stage.analysis_mode,
            input_mode=stage.input_mode,
            ordinal=ordinal,
            enabled_by_default=stage.enabled,
            runner_name=stage.runner_name or stage.stage_type.lower(),
            retry_policy_json={},
            resource_requirements_json={},
            metadata_json={},
        )
        session.add(record)
        session.flush()
        stage_records[stage.stage_key] = record
        for name, config_id in stage.configuration_inputs.items():
            session.add(
                m.PipelineStageConfigBinding(
                    stage_definition_id=record.id,
                    binding_name=name,
                    configuration_version_id=config_id,
                    required=True,
                )
            )
        for name, artifact_kind in stage.outputs.items():
            session.add(
                m.PipelineStageOutputDeclaration(
                    stage_definition_id=record.id,
                    output_name=name,
                    artifact_kind=artifact_kind,
                    required=True,
                    register_as_dataset=False,
                )
            )
    for stage in body.stages:
        for dependency in stage.depends_on:
            session.add(
                m.PipelineStageDependency(
                    stage_definition_id=stage_records[stage.stage_key].id,
                    depends_on_stage_definition_id=stage_records[dependency].id,
                )
            )
    add_audit(
        session,
        project_id=body.project_id,
        actor_user_id=user.id,
        action="PIPELINE_DEFINITION_CREATE",
        resource_type="PIPELINE_DEFINITION",
        resource_id=definition.id,
        request_id=request.state.request_id,
    )
    return {
        **model_dict(definition),
        "version": model_dict(version),
        "stages": canonical["stages"],
    }


@router.get("/pipeline-definition-versions/{version_id}")
def get_pipeline_definition_version(
    version_id: str,
    session: Session = Depends(get_session),
    user: RequestUser = Depends(get_current_user),
) -> dict:
    version = get_or_404(session, m.PipelineDefinitionVersion, version_id)
    definition = get_or_404(
        session, m.PipelineDefinition, version.pipeline_definition_id
    )
    require_project_role(session, user, definition.project_id)
    return model_dict(version)


@router.post(
    "/pipeline-definitions/{definition_id}/versions",
    status_code=status.HTTP_201_CREATED,
)
def create_pipeline_definition_version(
    definition_id: str,
    body: PipelineDefinitionVersionCreate,
    session: Session = Depends(get_session),
    user: RequestUser = Depends(get_current_user),
) -> dict:
    definition = get_or_404(session, m.PipelineDefinition, definition_id)
    require_project_role(session, user, definition.project_id, "ANALYST")
    keys = {stage.stage_key for stage in body.stages}
    if len(keys) != len(body.stages):
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY, "Stage keys must be unique"
        )
    if any(not set(stage.depends_on).issubset(keys) for stage in body.stages):
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            "Pipeline contains an unknown dependency",
        )
    canonical = {
        "random_seed_default": body.random_seed_default,
        "fail_fast": body.fail_fast,
        "stages": [stage.model_dump() for stage in body.stages],
    }
    digest = canonical_hash(canonical)
    existing = session.scalar(
        select(m.PipelineDefinitionVersion).where(
            m.PipelineDefinitionVersion.pipeline_definition_id == definition.id,
            m.PipelineDefinitionVersion.content_hash == digest,
        )
    )
    if existing:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            f"Identical pipeline already exists as version {existing.version_number}",
        )
    number = (
        session.scalar(
            select(func.max(m.PipelineDefinitionVersion.version_number)).where(
                m.PipelineDefinitionVersion.pipeline_definition_id == definition.id
            )
        )
        or 0
    ) + 1
    version = m.PipelineDefinitionVersion(
        pipeline_definition_id=definition.id,
        version_number=number,
        status="PUBLISHED" if body.publish else "DRAFT",
        random_seed_default=body.random_seed_default,
        fail_fast=body.fail_fast,
        canonical_json=canonical,
        content_hash=digest,
        created_by=user.id,
        published_at=m.utcnow() if body.publish else None,
    )
    session.add(version)
    session.flush()
    stage_records: dict[str, m.PipelineStageDefinition] = {}
    for ordinal, stage in enumerate(body.stages, start=1):
        record = m.PipelineStageDefinition(
            pipeline_definition_version_id=version.id,
            stage_key=stage.stage_key,
            stage_type=stage.stage_type,
            analysis_mode=stage.analysis_mode,
            input_mode=stage.input_mode,
            ordinal=ordinal,
            enabled_by_default=stage.enabled,
            runner_name=stage.runner_name or stage.stage_type.lower(),
            retry_policy_json={},
            resource_requirements_json={},
            metadata_json={},
        )
        session.add(record)
        session.flush()
        stage_records[stage.stage_key] = record
        for name, config_id in stage.configuration_inputs.items():
            session.add(
                m.PipelineStageConfigBinding(
                    stage_definition_id=record.id,
                    binding_name=name,
                    configuration_version_id=config_id,
                    required=True,
                )
            )
        for name, artifact_kind in stage.outputs.items():
            session.add(
                m.PipelineStageOutputDeclaration(
                    stage_definition_id=record.id,
                    output_name=name,
                    artifact_kind=artifact_kind,
                    required=True,
                    register_as_dataset=False,
                )
            )
    for stage in body.stages:
        for dependency in stage.depends_on:
            session.add(
                m.PipelineStageDependency(
                    stage_definition_id=stage_records[stage.stage_key].id,
                    depends_on_stage_definition_id=stage_records[dependency].id,
                )
            )
    return model_dict(version)


__all__ = ["router"]
