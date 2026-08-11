"""G6 project-scoped results, lineage, annotation, export, and workspace state."""

from __future__ import annotations

import hashlib
import tempfile
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from ariadne.product.domain.errors import (
    ArtifactHashMismatch,
    EntityNotFound,
    InvalidSchema,
    ProjectAccessDenied,
    ProjectBoundaryViolation,
)
from ariadne.product.domain.lineage import (
    LINEAGE_RELATION_TYPES,
    LineageAuthority,
    assert_generic_lineage_allowed,
    classify_lineage_authority,
)
from ariadne.product.domain.schemas import canonical_bytes
from ariadne.product.persistence.orm_models import (
    AnalysisSpecificationOrm,
    AnalysisViewOrm,
    AnnotationOrm,
    ArtifactOrm,
    DatasetVersionOrm,
    ExecutionOrm,
    ExportBundleOrm,
    FamilyArtifactOrm,
    FamilyExecutionOrm,
    FamilyResultOrm,
    GraphVersionOrm,
    LineageEdgeOrm,
    ProjectMembershipOrm,
    ProjectOrm,
    ResearchContextVersionOrm,
    ResultOrm,
    WorkspaceAnnotationOrm,
    WorkspaceSelectionOrm,
)
from ariadne.product.ports.artifact_store import ArtifactStorePort


READ_ROLES = frozenset({"OWNER", "EDITOR", "VIEWER"})
WRITE_ROLES = frozenset({"OWNER", "EDITOR"})
LINEAGE_RELATIONS = LINEAGE_RELATION_TYPES
ANNOTATION_TARGETS = frozenset({
    "Project", "ResearchContextVersion", "AnalysisView", "AnalysisSpecification",
    "Execution", "Result", "GraphVersion",
})
SECRET_TOKENS = ("secret", "password", "token", "api_key", "credential", "private_key")


def _now() -> datetime:
    return datetime.now(timezone.utc)


class ProductClosureService:
    def __init__(self, session_factory: Any, artifact_store: ArtifactStorePort) -> None:
        self._session_factory = session_factory
        self._artifact_store = artifact_store

    def register_project_owner(self, project_id: str, user_id: str) -> None:
        with self._session_factory() as session:
            if session.get(ProjectOrm, project_id) is None:
                raise EntityNotFound("Project", project_id)
            existing = session.scalar(select(ProjectMembershipOrm).where(
                ProjectMembershipOrm.project_id == project_id,
                ProjectMembershipOrm.user_id == user_id,
            ))
            if existing is None:
                session.add(ProjectMembershipOrm(
                    membership_id=str(uuid.uuid4()), project_id=project_id,
                    user_id=user_id, role="OWNER", created_at=_now(),
                ))
                session.commit()

    def set_member_role(
        self, project_id: str, user_id: str, role: str, *, actor_id: str
    ) -> dict[str, Any]:
        if role not in READ_ROLES:
            raise InvalidSchema("role must be OWNER, EDITOR, or VIEWER")
        with self._session_factory() as session:
            self._require_role(session, project_id, actor_id, {"OWNER"})
            row = session.scalar(select(ProjectMembershipOrm).where(
                ProjectMembershipOrm.project_id == project_id,
                ProjectMembershipOrm.user_id == user_id,
            ))
            if row is None:
                row = ProjectMembershipOrm(
                    membership_id=str(uuid.uuid4()), project_id=project_id,
                    user_id=user_id, role=role, created_at=_now(),
                )
                session.add(row)
            else:
                row.role = role
            session.commit()
            return {"project_id": project_id, "user_id": user_id, "role": role}

    def workspace_state(self, project_id: str, *, user_id: str) -> dict[str, Any]:
        with self._session_factory() as session:
            role = self._require_role(session, project_id, user_id, READ_ROLES)
            project = session.get(ProjectOrm, project_id)
            row = self._selection(session, project_id, user_id)
            return {
                "schema_version": "workspace-selection/1",
                "project": {
                    "project_id": project.project_id, "name": project.name,
                    "status": project.status, "topic": project.topic,
                    "objective": project.objective, "memo": project.memo,
                },
                "current_role": role,
                "research_context_version_id": row.research_context_version_id if row else None,
                "dataset_version_id": row.dataset_version_id if row else None,
                "analysis_view_id": row.analysis_view_id if row else None,
                "unsaved_draft": bool(row.unsaved_draft) if row else False,
                "updated_at": row.updated_at if row else None,
            }

    def update_workspace_state(
        self, project_id: str, changes: dict[str, Any], *, user_id: str
    ) -> dict[str, Any]:
        allowed = {
            "research_context_version_id", "dataset_version_id",
            "analysis_view_id", "unsaved_draft",
        }
        unknown = sorted(set(changes) - allowed)
        if unknown:
            raise InvalidSchema(f"Unknown workspace selection fields: {unknown}")
        with self._session_factory() as session:
            self._require_role(session, project_id, user_id, WRITE_ROLES)
            row = self._selection(session, project_id, user_id)
            if row is None:
                row = WorkspaceSelectionOrm(
                    workspace_selection_id=str(uuid.uuid4()), project_id=project_id,
                    user_id=user_id, unsaved_draft=False, updated_at=_now(),
                )
                session.add(row)
            for field in ("research_context_version_id", "dataset_version_id", "analysis_view_id"):
                if field in changes:
                    value = changes[field]
                    if value is not None:
                        expected = {
                            "research_context_version_id": "ResearchContextVersion",
                            "dataset_version_id": "DatasetVersion",
                            "analysis_view_id": "AnalysisView",
                        }[field]
                        self._assert_resource_project(session, expected, value, project_id)
                        if field == "research_context_version_id":
                            context = session.get(ResearchContextVersionOrm, value)
                            if context.status != "FIXED":
                                raise InvalidSchema("Active Research Context must be FIXED")
                        if field == "analysis_view_id":
                            view = session.get(AnalysisViewOrm, value)
                            if view.status != "FIXED":
                                raise InvalidSchema("Selected Analysis View must be FIXED")
                            if row.dataset_version_id is None:
                                row.dataset_version_id = view.source_dataset_version_id
                    setattr(row, field, value)
            if "unsaved_draft" in changes:
                row.unsaved_draft = bool(changes["unsaved_draft"])
            if row.analysis_view_id:
                view = session.get(AnalysisViewOrm, row.analysis_view_id)
                if row.dataset_version_id and view.source_dataset_version_id != row.dataset_version_id:
                    raise InvalidSchema("Selected Analysis View does not belong to selected Dataset Version")
            row.updated_at = _now()
            session.commit()
        return self.workspace_state(project_id, user_id=user_id)

    def list_results(self, project_id: str, *, user_id: str) -> list[dict[str, Any]]:
        with self._session_factory() as session:
            self._require_role(session, project_id, user_id, READ_ROLES)
            values = self._all_results(session, project_id)
            public = [self._public_result(item, include_sensitive=False, detail=False) for item in values]
            return sorted(public, key=lambda item: (str(item["created_at"]), item["result_id"]), reverse=True)

    def result_detail(
        self, project_id: str, result_id: str, *, user_id: str,
        include_sensitive: bool = False,
    ) -> dict[str, Any]:
        with self._session_factory() as session:
            role = self._require_role(session, project_id, user_id, READ_ROLES)
            if include_sensitive and role not in WRITE_ROLES:
                raise ProjectAccessDenied("Sensitive Result output requires OWNER or EDITOR role")
            value = self._public_result(
                self._find_result(session, project_id, result_id),
                include_sensitive=include_sensitive, detail=True,
            )
            value["annotations"] = self._annotation_values(session, project_id, "Result", result_id)
            return value

    def results_summary(self, project_id: str, *, user_id: str) -> dict[str, Any]:
        items = self.list_results(project_id, user_id=user_id)
        families: dict[str, int] = {}
        statuses: dict[str, int] = {}
        result_types: dict[str, int] = {}
        for item in items:
            families[item["analysis_family"]] = families.get(item["analysis_family"], 0) + 1
            statuses[item["analytical_status"]] = statuses.get(item["analytical_status"], 0) + 1
            result_types[item["result_type"]] = result_types.get(item["result_type"], 0) + 1
        return {
            "schema_version": "cross-analysis-result-summary/1",
            "project_id": project_id,
            "result_count": len(items),
            "by_family": families,
            "by_analytical_status": statuses,
            "by_result_type": result_types,
            "ranking": None,
            "warning": "Cross-family metrics are not normalized or ranked.",
        }

    def compare_results(
        self, project_id: str, result_ids: list[str], *, user_id: str
    ) -> dict[str, Any]:
        if len(result_ids) < 2 or len(result_ids) > 20 or len(set(result_ids)) != len(result_ids):
            raise InvalidSchema("comparison requires 2 to 20 distinct result_ids")
        with self._session_factory() as session:
            self._require_role(session, project_id, user_id, READ_ROLES)
            values = [self._find_result(session, project_id, value) for value in result_ids]
        families = {item["analysis_family"] for item in values}
        types = {item["result_type"] for item in values}
        if len(families) != 1 or len(types) != 1:
            raise InvalidSchema(
                "Quantitative comparison requires the same analysis family and compatible Result Type"
            )
        summaries = [_redact(item["summary"]) for item in values]
        keys = sorted(set().union(*(summary.keys() for summary in summaries)))
        common: dict[str, Any] = {}
        differences: list[dict[str, Any]] = []
        for key in keys:
            field_values = [summary.get(key) for summary in summaries]
            if all(value == field_values[0] for value in field_values):
                common[key] = field_values[0]
            else:
                differences.append({"field": key, "values": field_values})
        result_warnings = [list(item["warnings"]) for item in values]
        common_warnings = [
            warning for warning in result_warnings[0]
            if all(warning in warnings for warnings in result_warnings[1:])
        ]
        warning_differences = [
            {
                "result_id": item["result_id"],
                "warnings": [warning for warning in warnings if warning not in common_warnings],
            }
            for item, warnings in zip(values, result_warnings, strict=True)
        ]
        return _redact({
            "schema_version": "result-comparison/1",
            "project_id": project_id,
            "analysis_family": values[0]["analysis_family"],
            "result_type": values[0]["result_type"],
            "compatible": True,
            "common_summary": common,
            "differences": differences,
            "common_warnings": common_warnings,
            "warning_differences": warning_differences,
            "results": [{
                "result_id": item["result_id"],
                "analytical_status": item["analytical_status"],
                "summary": item["summary"],
                "warnings": item["warnings"],
            } for item in values],
            "ranking": None,
            "warnings": ["Compatible results are shown without cross-metric ranking."],
        })

    def project_lineage(self, project_id: str, *, user_id: str) -> dict[str, Any]:
        with self._session_factory() as session:
            self._require_role(session, project_id, user_id, READ_ROLES)
            nodes: dict[tuple[str, str], dict[str, Any]] = {}
            edges: dict[tuple[str, str, str, str, str], dict[str, Any]] = {}

            def node(kind: str, entity_id: str, label: str, **attributes: Any) -> None:
                nodes[(kind, entity_id)] = {
                    "node_type": kind, "entity_id": entity_id,
                    "label": label, "attributes": attributes,
                }

            def edge(source_type: str, source_id: str, relation: str,
                     target_type: str, target_id: str, *, explicit: bool = False,
                     source_class: str = "TYPED_STRUCTURAL",
                     evidence: dict[str, Any] | None = None) -> None:
                key = (source_type, source_id, relation, target_type, target_id)
                edges[key] = {
                    "source_type": source_type, "source_id": source_id,
                    "relation_type": relation, "target_type": target_type,
                    "target_id": target_id, "explicit": explicit,
                    "source_class": source_class,
                    "evidence": evidence or {},
                }

            project = session.get(ProjectOrm, project_id)
            node("Project", project_id, project.name, status=project.status)
            contexts = list(session.scalars(select(ResearchContextVersionOrm).where(ResearchContextVersionOrm.project_id == project_id)))
            datasets = list(session.scalars(select(DatasetVersionOrm).where(DatasetVersionOrm.project_id == project_id)))
            views = list(session.scalars(select(AnalysisViewOrm).where(AnalysisViewOrm.project_id == project_id)))
            specs = list(session.scalars(select(AnalysisSpecificationOrm).where(AnalysisSpecificationOrm.project_id == project_id)))
            for row in contexts:
                node("ResearchContextVersion", row.research_context_version_id, f"{row.context_key} v{row.version_number}", status=row.status)
            for row in datasets:
                node("DatasetVersion", row.dataset_version_id, f"{row.name} / {row.version_label}", content_hash=row.content_hash)
            for row in views:
                node("AnalysisView", row.analysis_view_id, f"{row.name} v{row.version_number}", status=row.status, content_hash=row.content_hash)
            for row in specs:
                node("AnalysisSpecification", row.analysis_specification_id, f"{row.analysis_family} {row.specification_key} v{row.version_number}", status=row.status)

            # TD-006 archive: retained historical rows are read-only inputs to
            # this derived projection, never Product lifecycle authority.
            family_execs = list(session.scalars(select(FamilyExecutionOrm).where(FamilyExecutionOrm.project_id == project_id)))
            for row in family_execs:
                node("Execution", row.execution_id, f"{row.analysis_family} Execution", family=row.analysis_family, status=row.status)
                edge("DatasetVersion", row.dataset_version_id, "USED_INPUT", "Execution", row.execution_id)
                if row.analysis_view_id:
                    edge("AnalysisView", row.analysis_view_id, "USED_INPUT", "Execution", row.execution_id)
            canonical_execs = list(session.scalars(select(ExecutionOrm).where(ExecutionOrm.project_id == project_id)))
            for row in canonical_execs:
                node("Execution", row.execution_id, f"{row.analysis_family} {row.operation}", family=row.analysis_family, status=row.status)
                edge("DatasetVersion", row.dataset_version_id, "USED_INPUT", "Execution", row.execution_id)
                analysis_view_id = row.analysis_spec_json.get("analysis_view_id")
                if isinstance(analysis_view_id, str) and analysis_view_id:
                    edge("AnalysisView", analysis_view_id, "USED_INPUT", "Execution", row.execution_id)
                if row.input_result_id:
                    edge("Result", row.input_result_id, "USED_INPUT", "Execution", row.execution_id)
                if row.base_execution_id:
                    relation = "REVISED_FROM" if row.revision_kind == "REVISED" else "DERIVED_FROM"
                    edge(
                        "Execution", row.base_execution_id, relation, "Execution", row.execution_id,
                        evidence={"revision_kind": row.revision_kind},
                    )
                else:
                    # TD-006 archive: compatibility read projection for
                    # canonical rows created before dedicated revision columns.
                    # It derives lineage only and must not write structural state.
                    revision = row.analysis_spec_json.get("revision_context") or {}
                    base_id = revision.get("base_execution_id") if isinstance(revision, dict) else None
                    if isinstance(base_id, str) and base_id:
                        edge(
                            "Execution", base_id, "REVISED_FROM", "Execution", row.execution_id,
                            evidence={"revision_context": revision},
                        )

            for item in self._all_results(session, project_id):
                node("Result", item["result_id"], item["result_type"], family=item["analysis_family"], analytical_status=item["analytical_status"])
                edge("Execution", item["execution_id"], "GENERATED", "Result", item["result_id"])
            legacy_artifacts = list(session.scalars(select(ArtifactOrm).where(ArtifactOrm.project_id == project_id)))
            family_artifacts = list(session.scalars(select(FamilyArtifactOrm).where(FamilyArtifactOrm.project_id == project_id)))
            for row in [*legacy_artifacts, *family_artifacts]:
                node("Artifact", row.artifact_id, row.artifact_type, content_hash=row.content_hash, media_type=row.media_type)
                if row.result_id:
                    edge("Result", row.result_id, "GENERATED", "Artifact", row.artifact_id)
            graphs = list(session.scalars(select(GraphVersionOrm).where(GraphVersionOrm.project_id == project_id)))
            for row in graphs:
                node("GraphVersion", row.graph_version_id, row.name, status=row.status, graph_origin=row.graph_origin)
                if row.source_result_id:
                    edge("Result", row.source_result_id, "DERIVED_FROM", "GraphVersion", row.graph_version_id)
            explicit_rows = list(session.scalars(select(LineageEdgeOrm).where(LineageEdgeOrm.project_id == project_id)))
            for row in explicit_rows:
                if classify_lineage_authority(
                    row.source_type, row.relation_type, row.target_type,
                ) is not LineageAuthority.GENERIC_ONLY:
                    continue
                if (row.source_type, row.source_id) not in nodes:
                    node(row.source_type, row.source_id, f"{row.source_type} {row.source_id}")
                if (row.target_type, row.target_id) not in nodes:
                    node(row.target_type, row.target_id, f"{row.target_type} {row.target_id}")
                edge(
                    row.source_type, row.source_id, row.relation_type, row.target_type, row.target_id,
                    explicit=True, source_class="GENERIC_ONLY", evidence=row.evidence_json,
                )
            return {
                "schema_version": "project-lineage/1", "project_id": project_id,
                "nodes": list(nodes.values()), "edges": list(edges.values()),
            }

    def result_lineage(self, project_id: str, result_id: str, *, user_id: str) -> dict[str, Any]:
        self.result_detail(project_id, result_id, user_id=user_id)
        graph = self.project_lineage(project_id, user_id=user_id)
        connected = {result_id}
        changed = True
        while changed:
            changed = False
            for item in graph["edges"]:
                if item["source_id"] in connected or item["target_id"] in connected:
                    before = len(connected)
                    connected.update((item["source_id"], item["target_id"]))
                    changed = changed or len(connected) != before
        return {
            **graph,
            "root_result_id": result_id,
            "nodes": [item for item in graph["nodes"] if item["entity_id"] in connected],
            "edges": [item for item in graph["edges"] if item["source_id"] in connected and item["target_id"] in connected],
        }

    @staticmethod
    def _public_result(
        item: dict[str, Any], *, include_sensitive: bool, detail: bool,
    ) -> dict[str, Any]:
        value = dict(item)
        value["summary"] = _redact(value.get("summary", {}))
        value["diagnostics"] = _redact(value.get("diagnostics", {}))
        value["warnings"] = _redact(value.get("warnings", []))
        if not detail:
            value.pop("payload", None)
            value.pop("diagnostics", None)
        elif not include_sensitive:
            value["payload"] = _suppress_sensitive_output(value.get("payload", {}))
            value["sensitive_output_suppressed"] = True
        else:
            value["sensitive_output_suppressed"] = False
        return value

    def create_lineage_link(
        self, project_id: str, payload: dict[str, Any], *, user_id: str
    ) -> dict[str, Any]:
        relation = str(payload.get("relation_type", ""))
        if relation not in LINEAGE_RELATIONS:
            raise InvalidSchema(f"Unsupported lineage relation_type: {relation}")
        source_type, source_id = str(payload.get("source_type", "")), str(payload.get("source_id", ""))
        target_type, target_id = str(payload.get("target_type", "")), str(payload.get("target_id", ""))
        if not all((source_type, source_id, target_type, target_id)):
            raise InvalidSchema("Lineage link requires source and target resource references")
        if (source_type, source_id) == (target_type, target_id):
            raise InvalidSchema("Lineage link cannot reference itself")
        with self._session_factory() as session:
            self._require_role(session, project_id, user_id, WRITE_ROLES)
            self._assert_resource_project(session, source_type, source_id, project_id)
            self._assert_resource_project(session, target_type, target_id, project_id)
            assert_generic_lineage_allowed(source_type, relation, target_type)
            row = LineageEdgeOrm(
                lineage_edge_id=str(uuid.uuid4()), project_id=project_id,
                source_type=source_type, source_id=source_id,
                relation_type=relation, target_type=target_type, target_id=target_id,
                evidence_json=dict(payload.get("evidence", {})), created_by=user_id,
                created_at=_now(),
            )
            session.add(row)
            try:
                session.commit()
            except IntegrityError:
                session.rollback()
                row = session.scalar(select(LineageEdgeOrm).where(
                    LineageEdgeOrm.source_type == source_type,
                    LineageEdgeOrm.source_id == source_id,
                    LineageEdgeOrm.relation_type == relation,
                    LineageEdgeOrm.target_type == target_type,
                    LineageEdgeOrm.target_id == target_id,
                ))
            return self._lineage_edge_value(row)

    def create_annotation(
        self, project_id: str, payload: dict[str, Any], *, user_id: str
    ) -> dict[str, Any]:
        target_type, target_id = str(payload.get("target_type", "")), str(payload.get("target_id", ""))
        if target_type not in ANNOTATION_TARGETS:
            raise InvalidSchema(f"Unsupported annotation target_type: {target_type}")
        statement = str(payload.get("statement", "")).strip()
        if not statement or len(statement) > 8000:
            raise InvalidSchema("statement must be 1 to 8000 characters")
        decision = payload.get("decision")
        if decision not in {None, "SELECTED", "REJECTED", "DEFERRED"}:
            raise InvalidSchema("decision must be SELECTED, REJECTED, DEFERRED, or null")
        with self._session_factory() as session:
            self._require_role(session, project_id, user_id, WRITE_ROLES)
            self._assert_resource_project(session, target_type, target_id, project_id)
            row = WorkspaceAnnotationOrm(
                annotation_id=str(uuid.uuid4()), project_id=project_id,
                target_type=target_type, target_id=target_id, statement=statement,
                rationale=payload.get("rationale"),
                assumptions_json=list(payload.get("assumptions", [])),
                limitations_json=list(payload.get("limitations", [])),
                decision=decision, next_actions_json=list(payload.get("next_actions", [])),
                revision_history_json=[], created_by=user_id,
                created_at=_now(), updated_at=_now(),
            )
            session.add(row)
            session.flush()
            if decision in {"SELECTED", "REJECTED"}:
                assert_generic_lineage_allowed(target_type, decision, "Annotation")
                session.add(LineageEdgeOrm(
                    lineage_edge_id=str(uuid.uuid4()), project_id=project_id,
                    source_type=target_type, source_id=target_id,
                    relation_type=decision, target_type="Annotation", target_id=row.annotation_id,
                    evidence_json={"rationale": row.rationale}, created_by=user_id,
                    created_at=_now(),
                ))
            session.commit()
            return self._annotation_value(row)

    def list_annotations(
        self, project_id: str, *, user_id: str,
        target_type: str | None = None, target_id: str | None = None,
    ) -> list[dict[str, Any]]:
        with self._session_factory() as session:
            self._require_role(session, project_id, user_id, READ_ROLES)
            return self._annotation_values(session, project_id, target_type, target_id)

    def update_annotation(
        self, project_id: str, annotation_id: str, changes: dict[str, Any], *, user_id: str
    ) -> dict[str, Any]:
        mutable = {"statement", "rationale", "assumptions", "limitations", "decision", "next_actions"}
        unknown = sorted(set(changes) - mutable)
        if unknown:
            raise InvalidSchema(f"Unknown annotation fields: {unknown}")
        with self._session_factory() as session:
            self._require_role(session, project_id, user_id, WRITE_ROLES)
            row = session.get(WorkspaceAnnotationOrm, annotation_id)
            if row is None or row.project_id != project_id:
                raise EntityNotFound("WorkspaceAnnotation", annotation_id)
            history = list(row.revision_history_json or [])
            history.append({
                "statement": row.statement, "rationale": row.rationale,
                "assumptions": row.assumptions_json, "limitations": row.limitations_json,
                "decision": row.decision, "next_actions": row.next_actions_json,
                "revised_by": user_id, "revised_at": _now().isoformat(),
            })
            if "statement" in changes:
                statement = str(changes["statement"]).strip()
                if not statement:
                    raise InvalidSchema("statement must not be empty")
                row.statement = statement
            for field, column in (
                ("rationale", "rationale"), ("assumptions", "assumptions_json"),
                ("limitations", "limitations_json"), ("decision", "decision"),
                ("next_actions", "next_actions_json"),
            ):
                if field in changes:
                    setattr(row, column, changes[field])
            if row.decision not in {None, "SELECTED", "REJECTED", "DEFERRED"}:
                raise InvalidSchema("Invalid annotation decision")
            row.revision_history_json = history
            row.updated_at = _now()
            session.commit()
            return self._annotation_value(row)

    def create_export(
        self, project_id: str, result_ids: list[str], *, user_id: str
    ) -> dict[str, Any]:
        if not result_ids or len(result_ids) > 100 or len(set(result_ids)) != len(result_ids):
            raise InvalidSchema("export requires 1 to 100 distinct result_ids")
        export_id = str(uuid.uuid4())
        object_key = f"projects/{project_id}/exports/{export_id}/manifest.json"
        lineage_references = self._export_lineage_references(project_id, result_ids, user_id=user_id)
        with self._session_factory() as session:
            self._require_role(session, project_id, user_id, WRITE_ROLES)
            results = [self._find_result(session, project_id, value) for value in result_ids]
            specification_ids = sorted({
                item["analysis_specification_id"] for item in results
                if item.get("analysis_specification_id")
            })
            specifications = []
            for value in specification_ids:
                row = session.get(AnalysisSpecificationOrm, value)
                if row is None:
                    continue
                specifications.append({
                    "analysis_specification_id": value,
                    "schema_version": row.schema_version,
                    "family_spec_schema_version": row.family_spec_schema_version,
                    "canonical_hash": row.canonical_hash,
                    "family_spec": _redact(row.family_spec_json),
                })
            artifacts = []
            for result_id in result_ids:
                for row in session.scalars(select(FamilyArtifactOrm).where(FamilyArtifactOrm.result_id == result_id)):
                    artifacts.append(self._artifact_value(row, "FAMILY"))
                for row in session.scalars(select(ArtifactOrm).where(ArtifactOrm.result_id == result_id)):
                    artifacts.append(self._artifact_value(row, "CAUSAL"))
            manifest = {
                "schema_version": "ariadne-export-manifest/1",
                "export_id": export_id,
                "project_id": project_id,
                "created_at": _now(),
                "created_by": user_id,
                "sensitive_rows_included": False,
                "results": [{
                    "result_id": item["result_id"], "analysis_family": item["analysis_family"],
                    "result_type": item["result_type"], "analytical_status": item["analytical_status"],
                    "summary": _redact(item["summary"]), "warnings": _redact(item["warnings"]),
                } for item in results],
                "specifications": specifications,
                "artifact_references": [{
                    key: value for key, value in item.items()
                    if key in {"artifact_id", "artifact_type", "schema_version", "content_hash", "media_type", "size_bytes"}
                } for item in artifacts],
                "lineage_references": lineage_references,
            }
            content = canonical_bytes(manifest)
            with tempfile.TemporaryDirectory() as directory:
                source = Path(directory) / "manifest.json"
                source.write_bytes(content)
                stored = self._artifact_store.store(source, object_key, "application/json")
            row = ExportBundleOrm(
                export_id=export_id, project_id=project_id,
                schema_version="ariadne-export-manifest/1", result_ids_json=result_ids,
                object_key=stored.object_key, content_hash=stored.content_hash,
                media_type=stored.media_type, size_bytes=stored.size_bytes,
                manifest_summary_json={
                    "result_count": len(results), "artifact_count": len(artifacts),
                    "lineage_reference_count": len(manifest["lineage_references"]),
                    "sensitive_rows_included": False,
                },
                created_by=user_id, created_at=_now(),
            )
            session.add(row)
            try:
                session.commit()
            except Exception:
                self._artifact_store.delete(stored.object_key)
                raise
            return self._export_value(row)

    def get_export(self, project_id: str, export_id: str, *, user_id: str) -> dict[str, Any]:
        with self._session_factory() as session:
            self._require_role(session, project_id, user_id, READ_ROLES)
            row = session.get(ExportBundleOrm, export_id)
            if row is None or row.project_id != project_id:
                raise EntityNotFound("ExportBundle", export_id)
            return self._export_value(row)

    def get_artifact(self, project_id: str, artifact_id: str, *, user_id: str) -> dict[str, Any]:
        with self._session_factory() as session:
            self._require_role(session, project_id, user_id, READ_ROLES)
            row, source = self._find_artifact(session, project_id, artifact_id)
            return self._artifact_value(row, source)

    def download_artifact(
        self, project_id: str, artifact_id: str, *, user_id: str
    ) -> tuple[dict[str, Any], bytes]:
        with self._session_factory() as session:
            self._require_role(session, project_id, user_id, READ_ROLES)
            row, source = self._find_artifact(session, project_id, artifact_id)
            value = self._artifact_value(row, source)
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "artifact"
            self._artifact_store.retrieve(row.object_key, target)
            content = target.read_bytes()
        if hashlib.sha256(content).hexdigest() != row.content_hash:
            raise ArtifactHashMismatch("Artifact content hash does not match persisted metadata")
        return value, content

    @staticmethod
    def _selection(session: Any, project_id: str, user_id: str) -> WorkspaceSelectionOrm | None:
        return session.scalar(select(WorkspaceSelectionOrm).where(
            WorkspaceSelectionOrm.project_id == project_id,
            WorkspaceSelectionOrm.user_id == user_id,
        ))

    @staticmethod
    def _require_role(session: Any, project_id: str, user_id: str, allowed: Iterable[str]) -> str:
        if session.get(ProjectOrm, project_id) is None:
            raise EntityNotFound("Project", project_id)
        membership = session.scalar(select(ProjectMembershipOrm).where(
            ProjectMembershipOrm.project_id == project_id,
            ProjectMembershipOrm.user_id == user_id,
        ))
        if membership is None or membership.role not in set(allowed):
            raise ProjectAccessDenied(f"User {user_id!r} cannot access Project {project_id!r}")
        return membership.role

    @staticmethod
    def _all_results(session: Any, project_id: str) -> list[dict[str, Any]]:
        values: list[dict[str, Any]] = []
        # TD-006 archive: Family rows are historical read-only compatibility
        # inputs. Canonical Result/Artifact rows own all current writes.
        family_rows = list(session.scalars(select(FamilyResultOrm).where(FamilyResultOrm.project_id == project_id)))
        for row in family_rows:
            execution = session.get(FamilyExecutionOrm, row.execution_id)
            artifacts = list(session.scalars(select(FamilyArtifactOrm).where(FamilyArtifactOrm.result_id == row.result_id)))
            values.append({
                "result_id": row.result_id, "project_id": project_id,
                "execution_id": row.execution_id, "analysis_family": row.analysis_family,
                "result_type": row.result_type, "schema_version": row.schema_version,
                "analytical_status": row.analytical_status, "summary": row.summary_json,
                "payload": row.payload_json, "diagnostics": row.diagnostics_json,
                "warnings": row.warning_json, "artifact_ids": [item.artifact_id for item in artifacts],
                "research_context_version_id": execution.research_context_version_id,
                "dataset_version_id": execution.dataset_version_id,
                "analysis_view_id": execution.analysis_view_id,
                "analysis_specification_id": execution.analysis_specification_id,
                "created_at": row.created_at,
            })
        canonical_rows = list(session.scalars(select(ResultOrm).join(
            ExecutionOrm, ResultOrm.execution_id == ExecutionOrm.execution_id
        ).where(ExecutionOrm.project_id == project_id)))
        for row in canonical_rows:
            execution = session.get(ExecutionOrm, row.execution_id)
            artifacts = list(session.scalars(select(ArtifactOrm).where(ArtifactOrm.result_id == row.result_id)))
            family_snapshot = dict(execution.runtime_version_json.get("family_snapshot", {}))
            values.append({
                "result_id": row.result_id, "project_id": project_id,
                "execution_id": row.execution_id, "analysis_family": execution.analysis_family,
                "result_type": row.result_type,
                "schema_version": row.payload_json.get("schema_version", "causal-result/1"),
                "analytical_status": row.scientific_status, "summary": row.summary_json,
                "payload": row.payload_json, "diagnostics": row.diagnostics_json,
                "warnings": row.warning_json, "artifact_ids": [item.artifact_id for item in artifacts],
                "research_context_version_id": family_snapshot.get("research_context", {}).get("id"),
                "dataset_version_id": execution.dataset_version_id,
                "analysis_view_id": execution.analysis_spec_json.get("analysis_view_id"),
                "analysis_specification_id": execution.analysis_spec_json.get("analysis_specification_id"),
                "created_at": row.created_at,
            })
        return values

    @classmethod
    def _find_result(cls, session: Any, project_id: str, result_id: str) -> dict[str, Any]:
        value = next((item for item in cls._all_results(session, project_id) if item["result_id"] == result_id), None)
        if value is None:
            raise EntityNotFound("Result", result_id)
        return value

    @classmethod
    def _assert_resource_project(
        cls, session: Any, resource_type: str, resource_id: str, project_id: str
    ) -> None:
        actual = cls._resource_project(session, resource_type, resource_id)
        if actual is None:
            raise EntityNotFound(resource_type, resource_id)
        if actual != project_id:
            raise ProjectBoundaryViolation(
                f"{resource_type} {resource_id!r} is not in Project {project_id!r}"
            )

    @classmethod
    def _resource_project(cls, session: Any, resource_type: str, resource_id: str) -> str | None:
        direct = {
            "Project": ProjectOrm,
            "ResearchContextVersion": ResearchContextVersionOrm,
            "DatasetVersion": DatasetVersionOrm,
            "AnalysisView": AnalysisViewOrm,
            "AnalysisSpecification": AnalysisSpecificationOrm,
            "GraphVersion": GraphVersionOrm,
            "Annotation": WorkspaceAnnotationOrm,
        }
        if resource_type in direct:
            row = session.get(direct[resource_type], resource_id)
            return (row.project_id if resource_type != "Project" else row.project_id) if row else None
        if resource_type == "Execution":
            row = session.get(FamilyExecutionOrm, resource_id) or session.get(ExecutionOrm, resource_id)
            return row.project_id if row else None
        if resource_type == "Result":
            family = session.get(FamilyResultOrm, resource_id)
            if family:
                return family.project_id
            legacy = session.get(ResultOrm, resource_id)
            execution = session.get(ExecutionOrm, legacy.execution_id) if legacy else None
            return execution.project_id if execution else None
        if resource_type == "Artifact":
            row = (
                session.get(FamilyArtifactOrm, resource_id)
                or session.get(ArtifactOrm, resource_id)
                or session.get(ExportBundleOrm, resource_id)
            )
            return row.project_id if row else None
        if resource_type == "FamilyArtifact":
            row = session.get(FamilyArtifactOrm, resource_id)
            return row.project_id if row else None
        return None

    @staticmethod
    def _lineage_edge_value(row: LineageEdgeOrm) -> dict[str, Any]:
        return {
            "lineage_edge_id": row.lineage_edge_id, "project_id": row.project_id,
            "source_type": row.source_type, "source_id": row.source_id,
            "relation_type": row.relation_type, "target_type": row.target_type,
            "target_id": row.target_id, "evidence": row.evidence_json,
            "created_by": row.created_by, "created_at": row.created_at,
        }

    @classmethod
    def _annotation_values(
        cls, session: Any, project_id: str,
        target_type: str | None = None, target_id: str | None = None,
    ) -> list[dict[str, Any]]:
        statement = select(WorkspaceAnnotationOrm).where(WorkspaceAnnotationOrm.project_id == project_id)
        if target_type is not None:
            statement = statement.where(WorkspaceAnnotationOrm.target_type == target_type)
        if target_id is not None:
            statement = statement.where(WorkspaceAnnotationOrm.target_id == target_id)
        return [cls._annotation_value(row) for row in session.scalars(statement.order_by(WorkspaceAnnotationOrm.created_at))]

    @staticmethod
    def _annotation_value(row: WorkspaceAnnotationOrm) -> dict[str, Any]:
        return {
            "annotation_id": row.annotation_id, "project_id": row.project_id,
            "target_type": row.target_type, "target_id": row.target_id,
            "statement": row.statement, "rationale": row.rationale,
            "assumptions": row.assumptions_json, "limitations": row.limitations_json,
            "decision": row.decision, "next_actions": row.next_actions_json,
            "revision_history": row.revision_history_json,
            "created_by": row.created_by, "created_at": row.created_at,
            "updated_at": row.updated_at,
        }

    @staticmethod
    def _artifact_value(row: Any, source: str) -> dict[str, Any]:
        return {
            "artifact_id": getattr(row, "artifact_id", getattr(row, "export_id", "")),
            "project_id": row.project_id, "source": source,
            "execution_id": getattr(row, "execution_id", None),
            "result_id": getattr(row, "result_id", None),
            "artifact_type": getattr(row, "artifact_type", "EXPORT_MANIFEST"),
            "schema_version": getattr(row, "schema_version", None),
            "content_hash": row.content_hash, "media_type": row.media_type,
            "size_bytes": row.size_bytes,
            "metadata": getattr(row, "metadata_json", getattr(row, "manifest_summary_json", {})),
            "created_at": row.created_at,
        }

    @staticmethod
    def _find_artifact(session: Any, project_id: str, artifact_id: str) -> tuple[Any, str]:
        for model, source in (
            (FamilyArtifactOrm, "FAMILY"), (ArtifactOrm, "CAUSAL"),
            (ExportBundleOrm, "EXPORT"),
        ):
            row = session.get(model, artifact_id)
            if row is not None:
                if row.project_id != project_id:
                    raise ProjectBoundaryViolation("Artifact is not in the requested Project")
                return row, source
        raise EntityNotFound("Artifact", artifact_id)

    @staticmethod
    def _export_value(row: ExportBundleOrm) -> dict[str, Any]:
        return {
            "export_id": row.export_id, "project_id": row.project_id,
            "schema_version": row.schema_version, "result_ids": row.result_ids_json,
            "artifact_id": row.export_id, "content_hash": row.content_hash,
            "media_type": row.media_type, "size_bytes": row.size_bytes,
            "manifest_summary": row.manifest_summary_json,
            "created_by": row.created_by, "created_at": row.created_at,
        }

    def _export_lineage_references(
        self, project_id: str, result_ids: list[str], *, user_id: str,
    ) -> list[dict[str, Any]]:
        """Reuse the authority-labelled closure; exports never infer authority."""
        references: dict[tuple[str, str, str, str, str], dict[str, Any]] = {}
        for result_id in result_ids:
            graph = self.result_lineage(project_id, result_id, user_id=user_id)
            for edge in graph["edges"]:
                key = (
                    edge["source_type"], edge["source_id"], edge["relation_type"],
                    edge["target_type"], edge["target_id"],
                )
                references.setdefault(key, dict(edge))
        return list(references.values())


def _redact(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: "[REDACTED]" if any(token in key.lower() for token in SECRET_TOKENS) else _redact(item)
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [_redact(item) for item in value]
    return value


def _suppress_sensitive_output(value: Any) -> Any:
    sensitive = {
        "local_explanation", "local_explanations", "local_contributions", "prediction_rows",
        "row_predictions", "row_contributions", "rows",
    }
    if isinstance(value, dict):
        return {
            key: "[SENSITIVE_OUTPUT_SUPPRESSED]" if key.lower() in sensitive
            else _suppress_sensitive_output(item)
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [_suppress_sensitive_output(item) for item in value]
    return value
