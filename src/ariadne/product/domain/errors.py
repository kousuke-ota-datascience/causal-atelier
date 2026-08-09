"""Domain errors for the product domain."""

from __future__ import annotations


class DomainError(Exception):
    pass


class EntityNotFound(DomainError):
    def __init__(self, entity: str, entity_id: str) -> None:
        super().__init__(f"{entity} not found: {entity_id}")
        self.entity = entity
        self.entity_id = entity_id


class ProjectBoundaryViolation(DomainError):
    pass


class ProjectAccessDenied(DomainError):
    pass


class ProjectArchived(DomainError):
    def __init__(self, project_id: str) -> None:
        super().__init__(f"Project is ARCHIVED and read-only: {project_id}")
        self.project_id = project_id


class InvalidStateTransition(DomainError):
    def __init__(self, entity: str, current: str, target: str) -> None:
        super().__init__(
            f"Cannot transition {entity} from {current!r} to {target!r}"
        )


class LegacyProductAuthorityDisabled(DomainError):
    """A retained legacy facade cannot perform Product lifecycle authority."""

    def __init__(self, operation: str) -> None:
        super().__init__(
            f"Legacy Family lifecycle authority is disabled for Product operation: {operation}"
        )
        self.operation = operation


class InvalidAnalysisSpec(DomainError):
    pass


class InvalidSchema(DomainError):
    """A versioned payload does not satisfy its canonical schema."""


class UnsupportedSchemaVersion(InvalidSchema):
    def __init__(self, schema_version: str) -> None:
        super().__init__(f"Unsupported schema version: {schema_version}")
        self.schema_version = schema_version


class ResourceImmutable(DomainError):
    pass


class InvalidExecutionPlan(DomainError):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code


class RunnerNotRegistered(InvalidExecutionPlan):
    def __init__(self, stage_type: str) -> None:
        super().__init__("RUNNER_NOT_REGISTERED", f"Runner is not registered: {stage_type}")


class DuplicateRegistration(DomainError):
    pass


class PredictiveValidationError(DomainError):
    def __init__(self, code: str, message: str, *, path: str | None = None) -> None:
        super().__init__(message)
        self.code = code
        self.path = path


class InvalidDatasetFile(DomainError):
    pass


class InvalidDatasetMetadata(DomainError):
    pass


class ScientificContractViolation(InvalidAnalysisSpec):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code


class GraphAlreadyFixed(DomainError):
    pass


class GraphParentNotFixed(DomainError):
    pass


class GraphOutcomeRequired(DomainError):
    pass


class GraphOutcomeMismatch(DomainError):
    pass


class InvalidGraphEditBase(DomainError):
    pass


class InvalidGraphSemantics(DomainError):
    pass


class UnsupportedAlgorithm(DomainError):
    def __init__(self, name: str) -> None:
        super().__init__(f"Unsupported algorithm: {name!r}")


class UnsupportedEstimator(DomainError):
    def __init__(self, name: str) -> None:
        super().__init__(f"Unsupported estimator: {name!r}")


class InfrastructureError(Exception):
    """Base class for technical failures that must not become Results."""


class ArtifactStoreUnavailable(InfrastructureError):
    pass


class ArtifactHashMismatch(InfrastructureError):
    pass


class OutputOwnershipError(DomainError):
    """Output metadata violates the canonical Result/Artifact ownership contract."""


class OutputCompensationError(InfrastructureError):
    """A failed output operation left physical locators for reconciliation."""

    def __init__(self, message: str, reconciliation: list[dict[str, str]]) -> None:
        super().__init__(message)
        self.reconciliation = reconciliation


class DatabaseUnavailable(InfrastructureError):
    pass


class ScientificCoreExecutionError(InfrastructureError):
    pass


class QueueClaimError(InfrastructureError):
    pass
