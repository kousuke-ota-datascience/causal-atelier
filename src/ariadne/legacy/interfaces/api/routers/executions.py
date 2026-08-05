"""Asynchronous execution lifecycle, event, artifact, and result endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Header, HTTPException, Request, Response, status
from fastapi.responses import FileResponse
from sqlalchemy import func, select
from ariadne.application.control_plane import ControlPlaneService as Session

from ariadne.application.run_execution import ExecutionService
from ariadne.application.run_execution.services import (
    ConflictError,
    ResourceNotFoundError,
    ValidationError,
    add_audit,
)
from ariadne.infrastructure.artifact_store import artifact_location
from ariadne.domain import metadata as m
from ariadne.interfaces.api.dependencies import (
    RequestUser,
    get_current_user,
    get_session,
    require_project_role,
)
from ariadne.interfaces.api.schemas import ExecutionCreate

from .common import get_or_404, model_dict


router = APIRouter(tags=["executions", "results", "artifacts"])


@router.post("/executions", status_code=status.HTTP_202_ACCEPTED)
def create_run(
    body: ExecutionCreate,
    response: Response,
    session: Session = Depends(get_session),
    user: RequestUser = Depends(get_current_user),
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
) -> dict:
    require_project_role(session, user, body.project_id, "ANALYST")
    try:
        run, reused = ExecutionService(session).create(
            request_document=body.model_dump(mode="json"),
            actor_user_id=user.id,
            idempotency_key=idempotency_key,
        )
    except ConflictError as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, str(exc)) from exc
    except ResourceNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except ValidationError as exc:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY, {"issues": exc.issues}
        ) from exc
    response.headers["Idempotency-Replayed"] = str(reused).lower()
    if body.execution_mode in {"DRY_RUN", "VALIDATE_ONLY"}:
        response.status_code = status.HTTP_200_OK
    return _run_response(session, run)


@router.get("/executions")
def list_runs(
    project_id: str,
    run_status: str | None = None,
    experiment_id: str | None = None,
    page: int = 1,
    limit: int = 50,
    session: Session = Depends(get_session),
    user: RequestUser = Depends(get_current_user),
) -> dict:
    require_project_role(session, user, project_id)
    page, limit = max(1, page), min(200, max(1, limit))
    query = select(m.Execution).where(m.Execution.project_id == project_id)
    if run_status:
        query = query.where(m.Execution.status == run_status)
    if experiment_id:
        query = query.where(m.Execution.experiment_id == experiment_id)
    total = session.scalar(select(func.count()).select_from(query.subquery())) or 0
    items = session.scalars(
        query.order_by(m.Execution.submitted_at.desc())
        .offset((page - 1) * limit)
        .limit(limit)
    ).all()
    return {
        "items": [model_dict(item) for item in items],
        "total": total,
        "page": page,
        "limit": limit,
    }


@router.get("/executions/{execution_id}")
def get_run(
    execution_id: str,
    session: Session = Depends(get_session),
    user: RequestUser = Depends(get_current_user),
) -> dict:
    run = get_or_404(session, m.Execution, execution_id)
    require_project_role(session, user, run.project_id)
    return _run_response(session, run)


@router.post("/executions/{execution_id}/cancel", status_code=status.HTTP_202_ACCEPTED)
def cancel_run(
    execution_id: str,
    request: Request,
    session: Session = Depends(get_session),
    user: RequestUser = Depends(get_current_user),
) -> dict:
    run = get_or_404(session, m.Execution, execution_id)
    require_project_role(session, user, run.project_id, "ANALYST")
    if run.status not in {"QUEUED", "VALIDATING", "RUNNING", "CANCEL_REQUESTED"}:
        raise HTTPException(
            status.HTTP_409_CONFLICT, f"Cannot cancel run in status {run.status}"
        )
    if run.status != "CANCEL_REQUESTED":
        run.status = "CANCEL_REQUESTED"
        run.cancel_requested_at = m.utcnow()
        ExecutionService(session).add_event(run.id, "CANCEL_REQUESTED", {"best_effort": True})
        session.add(
            m.OutboxEvent(
                aggregate_type="EXECUTION",
                aggregate_id=run.id,
                event_type="CANCEL_EXECUTION",
                payload_json={"execution_id": run.id},
            )
        )
        add_audit(
            session,
            project_id=run.project_id,
            actor_user_id=user.id,
            action="EXECUTION_CANCEL_REQUEST",
            resource_type="EXECUTION",
            resource_id=run.id,
            request_id=request.state.request_id,
        )
    return {"execution_id": run.id, "status": run.status, "best_effort": True}


@router.post("/executions/{execution_id}/retry", status_code=status.HTTP_202_ACCEPTED)
def retry_run(
    execution_id: str,
    session: Session = Depends(get_session),
    user: RequestUser = Depends(get_current_user),
) -> dict:
    run = get_or_404(session, m.Execution, execution_id)
    require_project_role(session, user, run.project_id, "ANALYST")
    try:
        retried = ExecutionService(session).retry(run, user.id)
    except ConflictError as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, str(exc)) from exc
    return _run_response(session, retried)


@router.get("/executions/{execution_id}/events")
def get_execution_events(
    execution_id: str,
    after_sequence: int = 0,
    limit: int = 500,
    session: Session = Depends(get_session),
    user: RequestUser = Depends(get_current_user),
) -> list[dict]:
    run = get_or_404(session, m.Execution, execution_id)
    require_project_role(session, user, run.project_id)
    events = session.scalars(
        select(m.ExecutionEvent)
        .where(m.ExecutionEvent.execution_id == run.id, m.ExecutionEvent.sequence_number > after_sequence)
        .order_by(m.ExecutionEvent.sequence_number)
        .limit(min(max(limit, 1), 1000))
    ).all()
    return [model_dict(event) for event in events]


@router.get("/executions/{execution_id}/artifacts")
def get_run_artifacts(
    execution_id: str,
    session: Session = Depends(get_session),
    user: RequestUser = Depends(get_current_user),
) -> list[dict]:
    run = get_or_404(session, m.Execution, execution_id)
    require_project_role(session, user, run.project_id)
    artifacts = session.scalars(
        select(m.Artifact)
        .join(
            m.StageExecutionArtifactOutput,
            m.StageExecutionArtifactOutput.artifact_id == m.Artifact.id,
        )
        .join(m.StageExecution, m.StageExecution.id == m.StageExecutionArtifactOutput.stage_execution_id)
        .where(m.StageExecution.execution_id == run.id)
        .order_by(m.Artifact.created_at)
    ).all()
    return [_artifact_response(item) for item in artifacts]


@router.get("/executions/{execution_id}/results")
def get_run_results(
    execution_id: str,
    session: Session = Depends(get_session),
    user: RequestUser = Depends(get_current_user),
) -> dict:
    run = get_or_404(session, m.Execution, execution_id)
    require_project_role(session, user, run.project_id)
    stages = session.scalars(
        select(m.StageExecution)
        .where(m.StageExecution.execution_id == run.id)
        .order_by(m.StageExecution.ordinal)
    ).all()
    items: list[dict] = []
    for stage in stages:
        candidates = (
            ("DISCOVERY", m.DiscoveryResult),
            ("EDGE_WEIGHT", m.EdgeWeightResult),
            ("TREATMENT_EFFECT", m.TreatmentEffectResult),
        )
        for result_type, model in candidates:
            result = session.scalar(
                select(model).where(model.stage_execution_id == stage.id)
            )
            if result:
                items.append(
                    {
                        "execution_id": run.id,
                        "stage_execution_id": stage.id,
                        "stage_key": stage.stage_key,
                        "result_type": result_type,
                        "result_id": result.id,
                        "status": getattr(result, "status", None)
                        or getattr(result, "diagnostic_status", None),
                        "created_at": model_dict(result).get("created_at"),
                        "url": {
                            "DISCOVERY": f"/api/v1/discovery-results/{result.id}",
                            "EDGE_WEIGHT": f"/api/v1/edge-weight-results/{result.id}",
                            "TREATMENT_EFFECT": f"/api/v1/treatment-effect-results/{result.id}",
                        }[result_type],
                    }
                )
    return {"execution_id": run.id, "items": items, "total": len(items)}


@router.get("/artifacts/{artifact_id}")
def get_artifact(
    artifact_id: str,
    session: Session = Depends(get_session),
    user: RequestUser = Depends(get_current_user),
) -> dict:
    artifact = get_or_404(session, m.Artifact, artifact_id)
    require_project_role(session, user, artifact.project_id)
    return _artifact_response(artifact)


@router.get("/artifacts/{artifact_id}/content")
def download_artifact(
    artifact_id: str,
    request: Request,
    session: Session = Depends(get_session),
    user: RequestUser = Depends(get_current_user),
) -> FileResponse:
    artifact = get_or_404(session, m.Artifact, artifact_id)
    require_project_role(session, user, artifact.project_id)
    if artifact.status != "AVAILABLE" or not artifact.stored_object_id:
        raise HTTPException(
            status.HTTP_409_CONFLICT, "Artifact content is not available"
        )
    stored = get_or_404(session, m.StoredObject, artifact.stored_object_id)
    path = request.app.state.artifact_store.resolve_local_path(
        artifact_location(stored)
    )
    add_audit(
        session,
        project_id=artifact.project_id,
        actor_user_id=user.id,
        action="ARTIFACT_DOWNLOAD",
        resource_type="ARTIFACT",
        resource_id=artifact.id,
        request_id=request.state.request_id,
    )
    return FileResponse(
        path, media_type=artifact.media_type, filename=artifact.logical_name
    )


@router.get("/artifacts/{artifact_id}/lineage")
def get_artifact_lineage(
    artifact_id: str,
    session: Session = Depends(get_session),
    user: RequestUser = Depends(get_current_user),
) -> dict:
    artifact = get_or_404(session, m.Artifact, artifact_id)
    require_project_role(session, user, artifact.project_id)
    upstream_rows = session.execute(
        select(m.ArtifactLineage, m.Artifact)
        .join(
            m.Artifact,
            m.Artifact.id == m.ArtifactLineage.upstream_artifact_id,
        )
        .where(m.ArtifactLineage.downstream_artifact_id == artifact.id)
    ).all()
    downstream_rows = session.execute(
        select(m.ArtifactLineage, m.Artifact)
        .join(
            m.Artifact,
            m.Artifact.id == m.ArtifactLineage.downstream_artifact_id,
        )
        .where(m.ArtifactLineage.upstream_artifact_id == artifact.id)
    ).all()
    return {
        "artifact": _artifact_response(artifact),
        "upstream": [
            {
                "relationship_type": lineage.relationship_type,
                "artifact": _artifact_response(relative),
            }
            for lineage, relative in upstream_rows
        ],
        "downstream": [
            {
                "relationship_type": lineage.relationship_type,
                "artifact": _artifact_response(relative),
            }
            for lineage, relative in downstream_rows
        ],
    }


@router.get("/discovery-results/{result_id}")
def get_discovery_result(
    result_id: str,
    algorithm: str | None = None,
    session: Session = Depends(get_session),
    user: RequestUser = Depends(get_current_user),
) -> dict:
    result = get_or_404(session, m.DiscoveryResult, result_id)
    stage = get_or_404(session, m.StageExecution, result.stage_execution_id)
    run = get_or_404(session, m.Execution, stage.execution_id)
    require_project_role(session, user, run.project_id)
    algorithms = session.scalars(
        select(m.DiscoveryAlgorithmResult).where(
            m.DiscoveryAlgorithmResult.discovery_result_id == result.id
        )
    ).all()
    if algorithm:
        algorithms = [item for item in algorithms if item.algorithm == algorithm]
    payload = model_dict(result)
    payload["algorithms"] = []
    for item in algorithms:
        edges = session.scalars(
            select(m.DiscoveryEdge).where(
                m.DiscoveryEdge.discovery_algorithm_result_id == item.id
            )
        ).all()
        payload["algorithms"].append(
            {**model_dict(item), "edges": [model_dict(edge) for edge in edges]}
        )
    payload["scientific_notice"] = (
        "Discovery edges are algorithm-dependent exploratory structures, not a proven true DAG."
    )
    return payload


@router.get("/edge-weight-results/{result_id}")
def get_edge_weight_result(
    result_id: str,
    session: Session = Depends(get_session),
    user: RequestUser = Depends(get_current_user),
) -> dict:
    result = get_or_404(session, m.EdgeWeightResult, result_id)
    stage = get_or_404(session, m.StageExecution, result.stage_execution_id)
    run = get_or_404(session, m.Execution, stage.execution_id)
    require_project_role(session, user, run.project_id)
    estimates = session.scalars(
        select(m.EdgeWeightEstimate).where(
            m.EdgeWeightEstimate.edge_weight_result_id == result.id
        )
    ).all()
    diagnostics = session.scalars(
        select(m.DiagnosticSummary).where(m.DiagnosticSummary.stage_execution_id == stage.id)
    ).all()
    return {
        **model_dict(result),
        "estimates": [model_dict(item) for item in estimates],
        "diagnostics": [model_dict(item) for item in diagnostics],
        "scientific_notice": "Edge weights are exploratory coefficients and are not identified causal effects.",
    }


@router.get("/treatment-effect-results/{result_id}")
def get_treatment_effect_result(
    result_id: str,
    session: Session = Depends(get_session),
    user: RequestUser = Depends(get_current_user),
) -> dict:
    result = get_or_404(session, m.TreatmentEffectResult, result_id)
    stage = get_or_404(session, m.StageExecution, result.stage_execution_id)
    run = get_or_404(session, m.Execution, stage.execution_id)
    require_project_role(session, user, run.project_id)
    estimates = session.scalars(
        select(m.TreatmentEffectEstimate).where(
            m.TreatmentEffectEstimate.treatment_effect_result_id == result.id
        )
    ).all()
    selected = session.scalars(
        select(m.SelectedAdjustmentVariable)
        .where(m.SelectedAdjustmentVariable.treatment_effect_result_id == result.id)
        .order_by(m.SelectedAdjustmentVariable.ordinal)
    ).all()
    excluded = session.scalars(
        select(m.ExcludedAdjustmentCandidate).where(
            m.ExcludedAdjustmentCandidate.treatment_effect_result_id == result.id
        )
    ).all()
    assumptions = session.scalars(
        select(m.CausalAssumption)
        .where(
            m.CausalAssumption.causal_design_version_id
            == result.causal_design_version_id
        )
        .order_by(m.CausalAssumption.ordinal)
    ).all()
    diagnostics = session.scalars(
        select(m.DiagnosticSummary).where(m.DiagnosticSummary.stage_execution_id == stage.id)
    ).all()
    return {
        **model_dict(result),
        "estimates": [model_dict(item) for item in estimates],
        "selected_adjustment_variables": [model_dict(item) for item in selected],
        "excluded_adjustment_candidates": [model_dict(item) for item in excluded],
        "assumptions": [model_dict(item) for item in assumptions],
        "diagnostics": [model_dict(item) for item in diagnostics],
        "scientific_notice": "Assumptions are declared or assessed by analysts; the service does not prove identification.",
    }


def _run_response(session: Session, run: m.Execution) -> dict:
    plan = session.get(m.ExecutionPlanRecord, run.id)
    stages = session.scalars(
        select(m.StageExecution)
        .where(m.StageExecution.execution_id == run.id)
        .order_by(m.StageExecution.ordinal)
    ).all()
    validations = session.scalars(
        select(m.ValidationExecution).where(m.ValidationExecution.execution_id == run.id)
    ).all()
    validation_payload = []
    for validation in validations:
        issues = session.scalars(
            select(m.ValidationIssueRecord)
            .where(m.ValidationIssueRecord.validation_execution_id == validation.id)
            .order_by(m.ValidationIssueRecord.ordinal)
        ).all()
        validation_payload.append(
            {
                **model_dict(validation),
                "issues": [model_dict(issue) for issue in issues],
            }
        )
    return {
        **model_dict(run),
        "execution_plan": plan.canonical_json if plan else None,
        "plan_hash": plan.plan_hash if plan else None,
        "stages": [model_dict(stage) for stage in stages],
        "validations": validation_payload,
    }


def _artifact_response(artifact: m.Artifact) -> dict:
    return {
        **model_dict(artifact, exclude={"stored_object_id"}),
        "content_url": f"/api/v1/artifacts/{artifact.id}/content"
        if artifact.status == "AVAILABLE"
        else None,
    }


__all__ = ["router"]
