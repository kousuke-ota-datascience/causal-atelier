"""Scientific target references for local studies."""
from dataclasses import dataclass

from ariadne.shared.content_ref import ContentRef


@dataclass(frozen=True)
class EstimandRef:
    family: str
    population: str
    contrast: str
    time: str | None = None
    target_ref: ContentRef | None = None

    def is_graph_structure(self) -> bool:
        return (self.family, self.population, self.contrast) == (
            "GRAPH_STRUCTURE", "OBSERVED_VARIABLES", "NOT_APPLICABLE",
        )
