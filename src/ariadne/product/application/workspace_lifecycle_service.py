"""G4 persistence-backed Research Context and Analysis Specification lifecycles."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any

from sqlalchemy import func, select

from ariadne.product.domain.analysis_specification import AnalysisSpecification
from ariadne.product.domain.enums import (
    AnalysisFamily,
    AnalysisMode,
    VersionedResourceStatus,
)
from ariadne.product.domain.errors import (
    EntityNotFound,
    InvalidSchema,
    ProjectArchived,
)
from ariadne.product.domain.research_context import ResearchContextVersion
from ariadne.product.domain.schemas import canonical_hash
from ariadne.product.persistence.orm_models import (
    AnalysisSpecificationOrm,
    AnalysisViewOrm,
    DatasetVersionOrm,
    FamilyExecutionOrm,
    FamilyResultOrm,
    ProjectOrm,
    ResearchContextVersionOrm,
)


class WorkspaceLifecycleService:
    def __init__(self, session_factory: Any) -> None:
        self._session_factory = session_factory

    def create_research_context(
        self,
        project_id: str,
        payload: dict[str, Any],
        *,
        created_by: str,
    ) -> dict[str, Any]:
        with self._session_factory() as session:
            self._active_project(session, project_id)
            context_key = _required_text("context_key", payload.get("context_key"), 100)
            version = (session.scalar(select(func.max(
                ResearchContextVersionOrm.version_number
            )).where(
                ResearchContextVersionOrm.project_id == project_id,
                ResearchContextVersionOrm.context_key == context_key,
            )) or 0) + 1
            domain = ResearchContextVersion(
                research_context_version_id=str(uuid.uuid4()),
                project_id=project_id,
                context_key=context_key,
                version_number=version,
                problem_statement=str(payload.get("problem_statement", "")),
                research_questions=list(payload.get("research_questions", [])),
                significance=payload.get("significance"),
                hypotheses=list(payload.get("hypotheses", [])),
                decision_context=dict(payload.get("decision_context", {})),
                relations=list(payload.get("relations", [])),
                created_by=created_by,
                created_at=_now(),
            )
            self._validate_context_json(domain)
            row = self._context_row(domain)
            session.add(row)
            session.commit()
            session.refresh(row)
            return self._context_response(row)

    def list_research_contexts(self, project_id: str) -> list[dict[str, Any]]:
        with self._session_factory() as session:
            self._project(session, project_id)
            rows = session.scalars(select(ResearchContextVersionOrm).where(
                ResearchContextVersionOrm.project_id == project_id
            ).order_by(
                ResearchContextVersionOrm.context_key,
                ResearchContextVersionOrm.version_number.desc(),
            ))
            return [self._context_response(row) for row in rows]

    def get_research_context(self, project_id: str, context_id: str) -> dict[str, Any]:
        with self._session_factory() as session:
            return self._context_response(self._context(session, project_id, context_id))

    def update_research_context(
        self, project_id: str, context_id: str, changes: dict[str, Any]
    ) -> dict[str, Any]:
        with self._session_factory() as session:
            self._active_project(session, project_id)
            row = self._context(session, project_id, context_id)
            domain = self._context_domain(row)
            domain.update(**changes)
            self._validate_context_json(domain)
            self._write_context(row, domain)
            session.commit()
            session.refresh(row)
            return self._context_response(row)

    def fix_research_context(self, project_id: str, context_id: str) -> dict[str, Any]:
        with self._session_factory() as session:
            self._active_project(session, project_id)
            row = self._context(session, project_id, context_id)
            domain = self._context_domain(row)
            for relation in domain.relations:
                target = self._context(
                    session, project_id, relation["target_context_version_id"]
                )
                if target.research_context_version_id == context_id:
                    raise InvalidSchema("Research Context cannot relate to itself")
            domain.fix()
            self._write_context(row, domain)
            row.fixed_at = _now()
            session.commit()
            session.refresh(row)
            return self._context_response(row)

    def research_context_usage(self, project_id: str, context_id: str) -> dict[str, Any]:
        with self._session_factory() as session:
            self._context(session, project_id, context_id)
            specifications = list(session.scalars(select(AnalysisSpecificationOrm).where(
                AnalysisSpecificationOrm.project_id == project_id,
                AnalysisSpecificationOrm.research_context_version_id == context_id,
            )))
            executions = list(session.scalars(select(FamilyExecutionOrm).where(
                FamilyExecutionOrm.project_id == project_id,
                FamilyExecutionOrm.research_context_version_id == context_id,
            )))
            execution_ids = [row.execution_id for row in executions]
            results = list(session.scalars(select(FamilyResultOrm).where(
                FamilyResultOrm.project_id == project_id,
                FamilyResultOrm.execution_id.in_(execution_ids),
            ))) if execution_ids else []
            return {
                "research_context_version_id": context_id,
                "analysis_specification_ids": [
                    row.analysis_specification_id for row in specifications
                ],
                "analysis_families": sorted({row.analysis_family for row in executions}),
                "execution_ids": execution_ids,
                "result_ids": [row.result_id for row in results],
            }

    def create_analysis_specification(
        self,
        project_id: str,
        payload: dict[str, Any],
        *,
        created_by: str,
    ) -> dict[str, Any]:
        with self._session_factory() as session:
            self._active_project(session, project_id)
            key = _required_text("specification_key", payload.get("specification_key"), 100)
            version = (session.scalar(select(func.max(
                AnalysisSpecificationOrm.version_number
            )).where(
                AnalysisSpecificationOrm.project_id == project_id,
                AnalysisSpecificationOrm.specification_key == key,
            )) or 0) + 1
            domain = self._new_specification(
                project_id,
                key,
                version,
                payload,
                created_by=created_by,
            )
            self._validate_specification_references(session, domain, require_fixed_context=False)
            row = self._specification_row(domain)
            session.add(row)
            session.commit()
            session.refresh(row)
            return self._specification_response(row)

    def list_analysis_specifications(self, project_id: str) -> list[dict[str, Any]]:
        with self._session_factory() as session:
            self._project(session, project_id)
            rows = session.scalars(select(AnalysisSpecificationOrm).where(
                AnalysisSpecificationOrm.project_id == project_id
            ).order_by(
                AnalysisSpecificationOrm.specification_key,
                AnalysisSpecificationOrm.version_number.desc(),
            ))
            return [self._specification_response(row) for row in rows]

    def get_analysis_specification(self, project_id: str, spec_id: str) -> dict[str, Any]:
        with self._session_factory() as session:
            return self._specification_response(self._specification(session, project_id, spec_id))

    def update_analysis_specification(
        self, project_id: str, spec_id: str, changes: dict[str, Any]
    ) -> dict[str, Any]:
        with self._session_factory() as session:
            self._active_project(session, project_id)
            row = self._specification(session, project_id, spec_id)
            domain = self._specification_domain(row)
            normalized = self._normalize_specification_changes(changes)
            domain.update(**normalized)
            self._validate_specification_references(session, domain, require_fixed_context=False)
            self._write_specification(row, domain)
            session.commit()
            session.refresh(row)
            return self._specification_response(row)

    def validate_analysis_specification(
        self, project_id: str, spec_id: str
    ) -> dict[str, Any]:
        with self._session_factory() as session:
            row = self._specification(session, project_id, spec_id)
            domain = self._specification_domain(row)
            self._validate_specification_references(session, domain, require_fixed_context=True)
            domain.validate()
            return {
                "analysis_specification_id": spec_id,
                "valid": True,
                "canonical_hash": canonical_hash(domain.envelope()),
                "warnings": domain.warnings,
            }

    def fix_analysis_specification(self, project_id: str, spec_id: str) -> dict[str, Any]:
        with self._session_factory() as session:
            self._active_project(session, project_id)
            row = self._specification(session, project_id, spec_id)
            domain = self._specification_domain(row)
            self._validate_specification_references(session, domain, require_fixed_context=True)
            domain.fix()
            self._write_specification(row, domain)
            row.fixed_at = _now()
            session.commit()
            session.refresh(row)
            return self._specification_response(row)

    def revise_analysis_specification(
        self,
        project_id: str,
        spec_id: str,
        *,
        changes: dict[str, Any],
        change_reason: str,
        created_by: str,
    ) -> dict[str, Any]:
        with self._session_factory() as session:
            self._active_project(session, project_id)
            base = self._specification(session, project_id, spec_id)
            if base.status != "FIXED":
                raise InvalidSchema("Only a FIXED Analysis Specification can be revised")
            reason = _required_text("change_reason", change_reason, 2000)
            version = (session.scalar(select(func.max(
                AnalysisSpecificationOrm.version_number
            )).where(
                AnalysisSpecificationOrm.project_id == project_id,
                AnalysisSpecificationOrm.specification_key == base.specification_key,
            )) or 0) + 1
            payload = self._specification_response(base)
            normalized = self._normalize_specification_changes(changes)
            for key, value in normalized.items():
                payload[key] = value
            payload["revision_context"] = {
                "base_analysis_specification_id": base.analysis_specification_id,
                "base_canonical_hash": base.canonical_hash,
                "change_reason": reason,
            }
            domain = self._new_specification(
                project_id,
                base.specification_key,
                version,
                payload,
                created_by=created_by,
            )
            self._validate_specification_references(session, domain, require_fixed_context=False)
            row = self._specification_row(domain)
            session.add(row)
            session.commit()
            session.refresh(row)
            return self._specification_response(row)

    @staticmethod
    def _new_specification(
        project_id: str,
        key: str,
        version: int,
        payload: dict[str, Any],
        *,
        created_by: str,
    ) -> AnalysisSpecification:
        try:
            family = AnalysisFamily(str(payload.get("analysis_family")))
            mode = AnalysisMode(str(payload.get("analysis_mode")))
        except ValueError as exc:
            raise InvalidSchema("Invalid analysis_family or analysis_mode") from exc
        return AnalysisSpecification(
            analysis_specification_id=str(uuid.uuid4()),
            project_id=project_id,
            specification_key=key,
            version_number=version,
            analysis_family=family,
            research_context_version_id=str(payload.get("research_context_version_id", "")),
            dataset_version_id=str(payload.get("dataset_version_id", "")),
            analysis_view_id=payload.get("analysis_view_id"),
            analysis_mode=mode,
            family_spec_schema_version=str(payload.get("family_spec_schema_version", "")),
            family_spec=dict(payload.get("family_spec", {})),
            revision_context=payload.get("revision_context"),
            warnings=list(payload.get("warnings", [])),
            created_by=created_by,
            created_at=_now(),
        )

    def _validate_specification_references(
        self,
        session: Any,
        domain: AnalysisSpecification,
        *,
        require_fixed_context: bool,
    ) -> None:
        context = self._context(
            session, domain.project_id, domain.research_context_version_id
        )
        if require_fixed_context and context.status != "FIXED":
            raise InvalidSchema("Analysis Specification requires a FIXED Research Context")
        dataset = session.get(DatasetVersionOrm, domain.dataset_version_id)
        if dataset is None or dataset.project_id != domain.project_id:
            raise EntityNotFound("DatasetVersion", domain.dataset_version_id)
        if domain.analysis_view_id:
            view = session.get(AnalysisViewOrm, domain.analysis_view_id)
            if view is None or view.project_id != domain.project_id:
                raise EntityNotFound("AnalysisView", domain.analysis_view_id)
            if view.status != "FIXED":
                raise InvalidSchema("Analysis Specification requires a FIXED Analysis View")
            if view.source_dataset_version_id != domain.dataset_version_id:
                raise InvalidSchema("Analysis View and Dataset Version do not match")

    @staticmethod
    def _normalize_specification_changes(changes: dict[str, Any]) -> dict[str, Any]:
        normalized = dict(changes)
        mutable = {
            "analysis_family",
            "research_context_version_id",
            "dataset_version_id",
            "analysis_view_id",
            "analysis_mode",
            "family_spec_schema_version",
            "family_spec",
            "revision_context",
            "warnings",
        }
        unknown = sorted(set(normalized) - mutable)
        if unknown:
            raise InvalidSchema(f"Unknown Analysis Specification fields: {unknown}")
        nullable = {"analysis_view_id", "revision_context"}
        invalid_nulls = sorted(
            key for key, value in normalized.items()
            if value is None and key not in nullable
        )
        if invalid_nulls:
            raise InvalidSchema(
                f"Analysis Specification fields cannot be null: {invalid_nulls}"
            )
        if "analysis_family" in normalized:
            try:
                normalized["analysis_family"] = AnalysisFamily(normalized["analysis_family"])
            except ValueError as exc:
                raise InvalidSchema("Invalid analysis_family") from exc
        if "analysis_mode" in normalized:
            try:
                normalized["analysis_mode"] = AnalysisMode(normalized["analysis_mode"])
            except ValueError as exc:
                raise InvalidSchema("Invalid analysis_mode") from exc
        return normalized

    @staticmethod
    def _validate_context_json(domain: ResearchContextVersion) -> None:
        canonical_hash(domain.snapshot())

    @staticmethod
    def _project(session: Any, project_id: str) -> ProjectOrm:
        project = session.get(ProjectOrm, project_id)
        if project is None:
            raise EntityNotFound("Project", project_id)
        return project

    @classmethod
    def _active_project(cls, session: Any, project_id: str) -> ProjectOrm:
        project = cls._project(session, project_id)
        if project.status == "ARCHIVED":
            raise ProjectArchived(project_id)
        return project

    @staticmethod
    def _context(
        session: Any, project_id: str, context_id: str
    ) -> ResearchContextVersionOrm:
        row = session.get(ResearchContextVersionOrm, context_id)
        if row is None or row.project_id != project_id:
            raise EntityNotFound("ResearchContextVersion", context_id)
        return row

    @staticmethod
    def _specification(
        session: Any, project_id: str, spec_id: str
    ) -> AnalysisSpecificationOrm:
        row = session.get(AnalysisSpecificationOrm, spec_id)
        if row is None or row.project_id != project_id:
            raise EntityNotFound("AnalysisSpecification", spec_id)
        return row

    @staticmethod
    def _context_domain(row: ResearchContextVersionOrm) -> ResearchContextVersion:
        return ResearchContextVersion(
            research_context_version_id=row.research_context_version_id,
            project_id=row.project_id,
            context_key=row.context_key,
            version_number=row.version_number,
            status=VersionedResourceStatus(row.status),
            problem_statement=row.problem_statement,
            research_questions=list(row.research_questions_json),
            significance=row.significance,
            hypotheses=list(row.hypotheses_json),
            decision_context=dict(row.decision_context_json),
            relations=list(row.relations_json),
            canonical_hash=row.canonical_hash,
            created_by=row.created_by,
            created_at=row.created_at,
        )

    @classmethod
    def _context_row(cls, domain: ResearchContextVersion) -> ResearchContextVersionOrm:
        row = ResearchContextVersionOrm(
            research_context_version_id=domain.research_context_version_id,
            project_id=domain.project_id,
            context_key=domain.context_key,
            version_number=domain.version_number,
            status=domain.status.value,
            schema_version="research-context/1",
            problem_statement=domain.problem_statement,
            research_questions_json=domain.research_questions,
            significance=domain.significance,
            hypotheses_json=domain.hypotheses,
            decision_context_json=domain.decision_context,
            relations_json=domain.relations,
            canonical_hash=domain.canonical_hash,
            created_by=domain.created_by,
            created_at=domain.created_at or _now(),
        )
        return row

    @staticmethod
    def _write_context(
        row: ResearchContextVersionOrm, domain: ResearchContextVersion
    ) -> None:
        row.status = domain.status.value
        row.problem_statement = domain.problem_statement
        row.research_questions_json = domain.research_questions
        row.significance = domain.significance
        row.hypotheses_json = domain.hypotheses
        row.decision_context_json = domain.decision_context
        row.relations_json = domain.relations
        row.canonical_hash = domain.canonical_hash

    @staticmethod
    def _context_response(row: ResearchContextVersionOrm) -> dict[str, Any]:
        return {
            "research_context_version_id": row.research_context_version_id,
            "project_id": row.project_id,
            "context_key": row.context_key,
            "version_number": row.version_number,
            "status": row.status,
            "schema_version": row.schema_version,
            "problem_statement": row.problem_statement,
            "research_questions": row.research_questions_json,
            "significance": row.significance,
            "hypotheses": row.hypotheses_json,
            "decision_context": row.decision_context_json,
            "relations": row.relations_json,
            "canonical_hash": row.canonical_hash,
            "created_by": row.created_by,
            "created_at": row.created_at,
            "fixed_at": row.fixed_at,
        }

    @staticmethod
    def _specification_domain(row: AnalysisSpecificationOrm) -> AnalysisSpecification:
        return AnalysisSpecification(
            analysis_specification_id=row.analysis_specification_id,
            project_id=row.project_id,
            specification_key=row.specification_key,
            version_number=row.version_number,
            status=VersionedResourceStatus(row.status),
            analysis_family=AnalysisFamily(row.analysis_family),
            research_context_version_id=row.research_context_version_id,
            dataset_version_id=row.dataset_version_id,
            analysis_view_id=row.analysis_view_id,
            analysis_mode=AnalysisMode(row.analysis_mode),
            family_spec_schema_version=row.family_spec_schema_version,
            family_spec=dict(row.family_spec_json),
            revision_context=row.revision_context_json,
            warnings=list(row.warnings_json),
            canonical_hash=row.canonical_hash,
            created_by=row.created_by,
            created_at=row.created_at,
        )

    @classmethod
    def _specification_row(cls, domain: AnalysisSpecification) -> AnalysisSpecificationOrm:
        return AnalysisSpecificationOrm(
            analysis_specification_id=domain.analysis_specification_id,
            project_id=domain.project_id,
            specification_key=domain.specification_key,
            version_number=domain.version_number,
            status=domain.status.value,
            schema_version="analysis-specification/1",
            analysis_family=domain.analysis_family.value,
            research_context_version_id=domain.research_context_version_id,
            dataset_version_id=domain.dataset_version_id,
            analysis_view_id=domain.analysis_view_id,
            analysis_mode=domain.analysis_mode.value,
            family_spec_schema_version=domain.family_spec_schema_version,
            family_spec_json=domain.family_spec,
            revision_context_json=domain.revision_context,
            warnings_json=domain.warnings,
            canonical_hash=domain.canonical_hash,
            created_by=domain.created_by,
            created_at=domain.created_at or _now(),
        )

    @staticmethod
    def _write_specification(
        row: AnalysisSpecificationOrm, domain: AnalysisSpecification
    ) -> None:
        row.status = domain.status.value
        row.analysis_family = domain.analysis_family.value
        row.research_context_version_id = domain.research_context_version_id
        row.dataset_version_id = domain.dataset_version_id
        row.analysis_view_id = domain.analysis_view_id
        row.analysis_mode = domain.analysis_mode.value
        row.family_spec_schema_version = domain.family_spec_schema_version
        row.family_spec_json = domain.family_spec
        row.revision_context_json = domain.revision_context
        row.warnings_json = domain.warnings
        row.canonical_hash = domain.canonical_hash

    @staticmethod
    def _specification_response(row: AnalysisSpecificationOrm) -> dict[str, Any]:
        return {
            "analysis_specification_id": row.analysis_specification_id,
            "project_id": row.project_id,
            "specification_key": row.specification_key,
            "version_number": row.version_number,
            "status": row.status,
            "schema_version": row.schema_version,
            "analysis_family": row.analysis_family,
            "research_context_version_id": row.research_context_version_id,
            "dataset_version_id": row.dataset_version_id,
            "analysis_view_id": row.analysis_view_id,
            "analysis_mode": row.analysis_mode,
            "family_spec_schema_version": row.family_spec_schema_version,
            "family_spec": row.family_spec_json,
            "revision_context": row.revision_context_json,
            "warnings": row.warnings_json,
            "canonical_hash": row.canonical_hash,
            "created_by": row.created_by,
            "created_at": row.created_at,
            "fixed_at": row.fixed_at,
        }


def _required_text(name: str, value: Any, maximum: int) -> str:
    if not isinstance(value, str) or not value.strip() or len(value.strip()) > maximum:
        raise InvalidSchema(f"{name} must be a non-empty string up to {maximum} characters")
    return value.strip()


def _now() -> datetime:
    return datetime.now(timezone.utc)
