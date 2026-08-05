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


class InvalidStateTransition(DomainError):
    def __init__(self, entity: str, current: str, target: str) -> None:
        super().__init__(
            f"Cannot transition {entity} from {current!r} to {target!r}"
        )


class InvalidAnalysisSpec(DomainError):
    pass


class GraphAlreadyFixed(DomainError):
    pass


class InvalidGraphSemantics(DomainError):
    pass


class UnsupportedAlgorithm(DomainError):
    def __init__(self, name: str) -> None:
        super().__init__(f"Unsupported algorithm: {name!r}")


class UnsupportedEstimator(DomainError):
    def __init__(self, name: str) -> None:
        super().__init__(f"Unsupported estimator: {name!r}")
