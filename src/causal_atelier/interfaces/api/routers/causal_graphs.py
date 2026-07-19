"""Server-persisted causal graph resources and immutable versions."""

from __future__ import annotations

import io
import json
import unicodedata
import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy import func, select

from causal_atelier.application.control_plane import ControlPlaneService as Session
from causal_atelier.application.run_execution.services import add_audit, canonical_hash
from causal_atelier.domain import metadata as m
from causal_atelier.interfaces.api.dependencies import (
    RequestUser,
    get_current_user,
    get_session,
    require_project_role,
)
from causal_atelier.interfaces.api.schemas import CausalGraphCreate, CausalGraphVersionCreate

from .common import get_or_404, model_dict, project_for_configuration_version


router = APIRouter(tags=["causal-graphs"])


@router.post("/causal-graphs", status_code=status.HTTP_201_CREATED)
def create_causal_graph(
    body: CausalGraphCreate,
    request: Request,
    session: Session = Depends(get_session),
    user: RequestUser = Depends(get_current_user),
) -> dict:
    require_project_role(session, user, body.project_id, "ANALYST")
    existing = session.scalar(
        select(m.CausalGraph).where(
            m.CausalGraph.project_id == body.project_id,
            func.lower(m.CausalGraph.slug) == body.slug.lower(),
        )
    )
    if existing:
        raise HTTPException(status.HTTP_409_CONFLICT, "Causal graph slug already exists")
    graph = m.CausalGraph(**body.model_dump(), created_by=user.id)
    session.add(graph)
    session.flush()
    add_audit(
        session,
        project_id=graph.project_id,
        actor_user_id=user.id,
        action="CAUSAL_GRAPH_CREATE",
        resource_type="CAUSAL_GRAPH",
        resource_id=graph.id,
        request_id=request.state.request_id,
    )
    return model_dict(graph)


@router.get("/causal-graphs")
def list_causal_graphs(
    project_id: str,
    page: int = 1,
    limit: int = 50,
    session: Session = Depends(get_session),
    user: RequestUser = Depends(get_current_user),
) -> dict:
    require_project_role(session, user, project_id)
    page, limit = max(1, page), min(200, max(1, limit))
    query = select(m.CausalGraph).where(
        m.CausalGraph.project_id == project_id, m.CausalGraph.deleted_at.is_(None)
    )
    total = session.scalar(select(func.count()).select_from(query.subquery())) or 0
    graphs = session.scalars(
        query.order_by(m.CausalGraph.updated_at.desc())
        .offset((page - 1) * limit)
        .limit(limit)
    ).all()
    return {
        "items": [_graph_response(session, graph) for graph in graphs],
        "total": total,
        "page": page,
        "limit": limit,
    }


@router.get("/causal-graphs/{graph_id}")
def get_causal_graph(
    graph_id: str,
    session: Session = Depends(get_session),
    user: RequestUser = Depends(get_current_user),
) -> dict:
    graph = get_or_404(session, m.CausalGraph, graph_id)
    require_project_role(session, user, graph.project_id)
    return _graph_response(session, graph)


@router.post(
    "/causal-graphs/{graph_id}/versions", status_code=status.HTTP_201_CREATED
)
def create_causal_graph_version(
    graph_id: str,
    body: CausalGraphVersionCreate,
    request: Request,
    session: Session = Depends(get_session),
    user: RequestUser = Depends(get_current_user),
) -> dict:
    graph = get_or_404(session, m.CausalGraph, graph_id)
    require_project_role(session, user, graph.project_id, "ANALYST")
    algorithm_result = get_or_404(
        session, m.DiscoveryAlgorithmResult, body.source_discovery_algorithm_result_id
    )
    discovery = get_or_404(
        session, m.DiscoveryResult, algorithm_result.discovery_result_id
    )
    stage = get_or_404(session, m.StageRun, discovery.stage_run_id)
    run = get_or_404(session, m.Run, stage.run_id)
    semantics = get_or_404(
        session, m.ConfigurationVersion, body.feature_semantics_version_id
    )
    semantics_project = project_for_configuration_version(session, semantics)
    semantics_binding = session.get(m.FeatureSemanticsDatasetBinding, semantics.id)
    if (
        run.project_id != graph.project_id
        or semantics_project != graph.project_id
        or semantics.status != "PUBLISHED"
        or not semantics_binding
        or semantics_binding.dataset_version_id != discovery.dataset_version_id
    ):
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            "Discovery, Dataset, and published Feature Semantics must share one project and dataset",
        )
    discovery_edges = session.scalars(
        select(m.DiscoveryEdge).where(
            m.DiscoveryEdge.discovery_algorithm_result_id == algorithm_result.id,
            m.DiscoveryEdge.selected.is_(True),
        )
    ).all()
    roles = {
        item.name: item.role
        for item in session.scalars(
            select(m.FeatureSemanticItem).where(
                m.FeatureSemanticItem.feature_semantics_version_id == semantics.id
            )
        ).all()
    }
    canonical_edges = [_canonical_edge(edge) for edge in discovery_edges]
    canonical_edges.sort(key=lambda edge: (edge["node_a"], edge["node_b"]))
    nodes = sorted(
        set(algorithm_result.metadata_json.get("node_names", []))
        | {
            endpoint
            for edge in canonical_edges
            for endpoint in (edge["node_a"], edge["node_b"])
        }
    )
    document = {
        "schema_version": "1",
        "nodes": [{"name": name, "role": roles.get(name)} for name in nodes],
        "edges": canonical_edges,
    }
    digest = canonical_hash(document)
    existing = session.scalar(
        select(m.CausalGraphVersion).where(
            m.CausalGraphVersion.causal_graph_id == graph.id,
            m.CausalGraphVersion.content_hash == digest,
        )
    )
    if existing:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            f"Identical graph already exists as version {existing.version_number}",
        )
    payload = json.dumps(
        document, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    object_key = f"saved-graphs/{graph.project_id}/{graph.id}/{uuid.uuid4()}.json"
    stored = request.app.state.artifact_store.put_stream(
        io.BytesIO(payload), key=object_key
    )
    stored_object = m.StoredObject(
        backend=stored.location.backend,
        bucket=stored.location.namespace,
        object_key=stored.location.key,
        object_version=stored.location.version or "",
        media_type="application/json",
        format="JSON",
        size_bytes=stored.size_bytes,
        checksum=stored.checksum,
        status="AVAILABLE",
    )
    session.add(stored_object)
    session.flush()
    artifact = m.Artifact(
        project_id=graph.project_id,
        artifact_kind="SAVED_CAUSAL_GRAPH",
        logical_name=f"{graph.slug}-v{_next_version_number(session, graph.id)}.json",
        status="AVAILABLE",
        stored_object_id=stored_object.id,
        media_type="application/json",
        schema_name="saved-causal-graph",
        schema_version="1",
        content_hash=stored.checksum,
        metadata_json={"causal_graph_id": graph.id},
    )
    session.add(artifact)
    session.flush()
    number = _next_version_number(session, graph.id)
    version = m.CausalGraphVersion(
        causal_graph_id=graph.id,
        version_number=number,
        status="VALID",
        source_discovery_algorithm_result_id=algorithm_result.id,
        dataset_version_id=discovery.dataset_version_id,
        feature_semantics_version_id=semantics.id,
        algorithm=algorithm_result.algorithm,
        algorithm_parameter_hash=canonical_hash(algorithm_result.metadata_json),
        node_count=len(nodes),
        edge_count=len(canonical_edges),
        canonical_json=document,
        content_hash=digest,
        graph_artifact_id=artifact.id,
        selection_note=body.selection_note,
        created_by=user.id,
        validated_at=m.utcnow(),
    )
    session.add(version)
    session.flush()
    for ordinal, name in enumerate(nodes, start=1):
        session.add(
            m.CausalGraphNode(
                causal_graph_version_id=version.id,
                name=name,
                ordinal=ordinal,
                role_snapshot=roles.get(name),
                metadata_json={},
            )
        )
    by_pair = {
        (canonical["node_a"], canonical["node_b"]): edge
        for edge in discovery_edges
        for canonical in (_canonical_edge(edge),)
    }
    for raw in canonical_edges:
        source_edge = by_pair.get((raw["node_a"], raw["node_b"]))
        session.add(
            m.CausalGraphEdge(
                causal_graph_version_id=version.id,
                source_discovery_edge_id=source_edge.id if source_edge else None,
                payload_json=raw.get("payload", {}),
                **{key: raw.get(key) for key in (
                    "node_a", "node_b", "endpoint_at_a", "endpoint_at_b", "score", "stability"
                )},
            )
        )
    if algorithm_result.edge_artifact_id:
        session.add(
            m.ArtifactLineage(
                downstream_artifact_id=artifact.id,
                upstream_artifact_id=algorithm_result.edge_artifact_id,
                relationship_type="SELECTED_FROM",
            )
        )
    graph.updated_at = m.utcnow()
    add_audit(
        session,
        project_id=graph.project_id,
        actor_user_id=user.id,
        action="CAUSAL_GRAPH_VERSION_CREATE",
        resource_type="CAUSAL_GRAPH_VERSION",
        resource_id=version.id,
        request_id=request.state.request_id,
        after={"content_hash": digest, "source_algorithm": algorithm_result.algorithm},
    )
    return _version_response(session, version)


@router.get("/causal-graph-versions/{version_id}")
def get_causal_graph_version(
    version_id: str,
    session: Session = Depends(get_session),
    user: RequestUser = Depends(get_current_user),
) -> dict:
    version = get_or_404(session, m.CausalGraphVersion, version_id)
    graph = get_or_404(session, m.CausalGraph, version.causal_graph_id)
    require_project_role(session, user, graph.project_id)
    return _version_response(session, version)


@router.post("/causal-graph-versions/{version_id}/publish")
def publish_causal_graph_version(
    version_id: str,
    request: Request,
    session: Session = Depends(get_session),
    user: RequestUser = Depends(get_current_user),
) -> dict:
    version = get_or_404(session, m.CausalGraphVersion, version_id)
    graph = get_or_404(session, m.CausalGraph, version.causal_graph_id)
    require_project_role(session, user, graph.project_id, "ANALYST")
    if version.status != "VALID":
        raise HTTPException(
            status.HTTP_409_CONFLICT, "Only VALID graph versions can be published"
        )
    version.status = "PUBLISHED"
    version.published_by = user.id
    version.published_at = m.utcnow()
    add_audit(
        session,
        project_id=graph.project_id,
        actor_user_id=user.id,
        action="CAUSAL_GRAPH_VERSION_PUBLISH",
        resource_type="CAUSAL_GRAPH_VERSION",
        resource_id=version.id,
        request_id=request.state.request_id,
    )
    return _version_response(session, version)


def _graph_response(session: Session, graph: m.CausalGraph) -> dict:
    versions = session.scalars(
        select(m.CausalGraphVersion)
        .where(m.CausalGraphVersion.causal_graph_id == graph.id)
        .order_by(m.CausalGraphVersion.version_number.desc())
    ).all()
    return {**model_dict(graph), "versions": [model_dict(item) for item in versions]}


def _version_response(session: Session, version: m.CausalGraphVersion) -> dict:
    nodes = session.scalars(
        select(m.CausalGraphNode)
        .where(m.CausalGraphNode.causal_graph_version_id == version.id)
        .order_by(m.CausalGraphNode.ordinal)
    ).all()
    edges = session.scalars(
        select(m.CausalGraphEdge)
        .where(m.CausalGraphEdge.causal_graph_version_id == version.id)
        .order_by(m.CausalGraphEdge.node_a, m.CausalGraphEdge.node_b)
    ).all()
    return {
        **model_dict(version),
        "nodes": [model_dict(node) for node in nodes],
        "edges": [model_dict(edge) for edge in edges],
    }


def _next_version_number(session: Session, graph_id: str) -> int:
    return (
        session.scalar(
            select(func.max(m.CausalGraphVersion.version_number)).where(
                m.CausalGraphVersion.causal_graph_id == graph_id
            )
        )
        or 0
    ) + 1


def _canonical_edge(edge: m.DiscoveryEdge) -> dict[str, Any]:
    source = unicodedata.normalize("NFC", edge.source)
    target = unicodedata.normalize("NFC", edge.target)
    payload = dict(edge.payload_json or {})
    left = _endpoint(payload.get("endpoint_source"), edge.orientation, source_side=True)
    right = _endpoint(payload.get("endpoint_target"), edge.orientation, source_side=False)
    if source > target:
        source, target, left, right = target, source, right, left
    return {
        "node_a": source,
        "node_b": target,
        "endpoint_at_a": left,
        "endpoint_at_b": right,
        "score": edge.score,
        "stability": edge.stability,
        "payload": payload,
    }


def _endpoint(value: Any, orientation: str | None, *, source_side: bool) -> str:
    normalized = str(value or "").upper()
    if normalized in {"TAIL", "ARROW", "CIRCLE"}:
        return normalized
    text = str(orientation or "").lower()
    if "undirected" in text:
        return "TAIL"
    if "bidirected" in text:
        return "ARROW"
    return "TAIL" if source_side else "ARROW"


__all__ = ["router"]
