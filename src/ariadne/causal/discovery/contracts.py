"""P04 immutable verified input and typed Discovery result."""
from __future__ import annotations

import hashlib
import json
from collections.abc import Callable
from dataclasses import InitVar, dataclass, field
from typing import TYPE_CHECKING

from ariadne.capabilities.causal.ports.content_ref import VerifiedContent
from ariadne.causal.design.study import ValidatedStudy
from ariadne.causal.discovery.graph_evidence import GraphEvidence
from ariadne.scientific.capabilities import BackendCapabilityRecord, unsupported
from ariadne.scientific.ports.capability import ValidatedCapabilityRequest
from ariadne.scientific.ports.artifacts import ArtifactDescriptorView
from ariadne.shared.content_ref import nonempty_text
from ariadne.shared.serialization import jcs

if TYPE_CHECKING:
    from ariadne.scientific.causal_methods.fci_eligibility import EligibilityEvidence

_INT64_MIN = -(1 << 63)
_INT64_MAX = (1 << 63) - 1


def exact_integer(value: object) -> bool:
    return type(value) is int and _INT64_MIN <= value <= _INT64_MAX


def exact_fields(value: object, names: str) -> dict:
    if type(value) is not dict or set(value) != set(names.split()):
        raise unsupported("Unexpected or absent scientific input properties")
    return value


def read_evidence(content: VerifiedContent) -> object:
    try:
        def reject_constant(_value):
            raise ValueError("Non-JSON number")
        return json.loads(content.data.decode("utf-8"), object_pairs_hook=jcs.unique_object,
                          parse_constant=reject_constant)
    except (ValueError, RecursionError) as error:
        raise unsupported("Invalid strict scientific JSON") from error


@dataclass(frozen=True)
class DiscoveryVariable:
    name: str
    scale: str
    category_codes: tuple[int, ...] | None

    def __post_init__(self) -> None:
        if not nonempty_text(self.name):
            raise unsupported("Invalid Design variable name")
        codes = self.category_codes
        if self.scale == "CONTINUOUS" and codes is None:
            return
        if (
            self.scale != "CATEGORICAL" or type(codes) is not tuple or len(codes) < 2
            or not all(exact_integer(code) for code in codes)
            or any(left >= right for left, right in zip(codes, codes[1:]))
        ):
            raise unsupported("Invalid declared categorical domain")


@dataclass(frozen=True)
class DiscoveryDesign:
    question_id: str
    variables: tuple[DiscoveryVariable, ...]
    assumptions: tuple[str, ...]

    def __post_init__(self) -> None:
        if (
            not nonempty_text(self.question_id) or type(self.variables) is not tuple
            or len(self.variables) < 2 or not all(type(item) is DiscoveryVariable for item in self.variables)
            or len(set(self.columns)) != len(self.variables)
            or len({item.scale for item in self.variables}) != 1
            or type(self.assumptions) is not tuple or not all(nonempty_text(item) for item in self.assumptions)
        ):
            raise unsupported("Invalid Design identity, variables or declared assumptions")

    @property
    def columns(self) -> tuple[str, ...]:
        return tuple(item.name for item in self.variables)

    @property
    def measurement_scale(self) -> str:
        return self.variables[0].scale

    @classmethod
    def from_payload(cls, raw: object, *, question_id: str, background_knowledge: object) -> DiscoveryDesign:
        design = exact_fields(raw, "design_id question_id design_kind variables assumptions background_knowledge")
        if (
            not nonempty_text(design["design_id"]) or design["question_id"] != question_id
            or design["design_kind"] != "OBSERVATIONAL_GRAPH_DISCOVERY"
            or jcs.canonical_bytes(design["background_knowledge"]) != jcs.canonical_bytes(background_knowledge)
            or type(design["variables"]) is not list
        ):
            raise unsupported("Design evidence does not match Study")
        variables = []
        for raw_variable in design["variables"]:
            categorical = type(raw_variable) is dict and raw_variable.get("measurement_scale") == "CATEGORICAL"
            item = exact_fields(raw_variable,
                                "name measurement_scale category_codes" if categorical else "name measurement_scale")
            codes = item.get("category_codes")
            if categorical and type(codes) is not list:
                raise unsupported("Category codes must be an array of integers")
            variables.append(DiscoveryVariable(item["name"], item["measurement_scale"],
                                               tuple(codes) if categorical else None))
        assumptions = exact_fields(design["assumptions"], "causal_markov_declared faithfulness_declared "
                                   "acyclicity_declared latent_confounding_possible sampling_unit")
        labels = ("causal_markov_declared", "faithfulness_declared", "acyclicity_declared",
                  "latent_confounding_possible")
        if not nonempty_text(assumptions["sampling_unit"]) or any(type(assumptions[key]) is not bool for key in labels):
            raise unsupported("Invalid declared sampling assumptions")
        return cls(question_id, tuple(variables), tuple(key for key in labels if assumptions[key]))


@dataclass(frozen=True)
class ValidatedDiscoveryRequest:
    capability_request: ValidatedCapabilityRequest
    capability: BackendCapabilityRecord
    question: VerifiedContent = field(repr=False)
    design: VerifiedContent = field(repr=False)
    dataset: VerifiedContent = field(repr=False)
    decode_dataset: InitVar[Callable]
    columns: tuple[str, ...] = field(init=False)
    rows: tuple[tuple[int | float, ...], ...] = field(init=False, repr=False)

    def __post_init__(self, decode_dataset: Callable) -> None:
        cap = self.capability_request
        self.capability.check(cap)
        wire = cap.study.to_payload()
        for name in ("question", "design", "dataset"):
            evidence = getattr(self, name)
            if (
                type(evidence) is not VerifiedContent or evidence.ref != getattr(cap.study, name)
                or type(evidence.data) is not bytes or evidence.size_bytes != len(evidence.data)
                or hashlib.sha256(evidence.data).hexdigest() != evidence.ref.sha256
            ):
                raise unsupported("Verified Discovery input does not match the Study ContentRef")
        question = exact_fields(read_evidence(self.question), "question_id research_question population analysis_goal")
        if (
            self.question.ref.schema_version is not None or self.design.ref.schema_version is not None
            or question["question_id"] != self.question.ref.identity or question["analysis_goal"] != "GRAPH_STRUCTURE"
            or not nonempty_text(question["research_question"]) or not nonempty_text(question["population"])
        ):
            raise unsupported("Question evidence does not match Study")
        design = DiscoveryDesign.from_payload(
            read_evidence(self.design), question_id=question["question_id"],
            background_knowledge=wire["method"]["config"]["background_knowledge"],
        )
        # The trusted Dataset decoder receives the exact ContentRef-verified bytes.
        columns, rows = decode_dataset(self.dataset)
        if (
            design != cap.design or type(columns) is not tuple or columns != design.columns
            or type(rows) is not tuple or not rows
            or not all(type(row) is tuple and len(row) == len(columns)
                       and all(type(value) in (int, float) for value in row) for row in rows)
        ):
            raise unsupported("Dataset columns or rows do not match validated Design")
        object.__setattr__(self, "columns", columns)
        object.__setattr__(self, "rows", rows)

    @property
    def study(self) -> ValidatedStudy:
        return self.capability_request.study

    @property
    def seed(self) -> int | None:
        return self.study.to_payload()["randomness"]["seed"]

    @property
    def upstream_digests(self) -> tuple[str, str, str]:
        return self.question.ref.sha256, self.design.ref.sha256, self.dataset.ref.sha256


@dataclass(frozen=True)
class DiscoveryGraphOutcome:
    """G01 Graph-success. Technical failures are typed exceptions."""
    graph: GraphEvidence
    artifact: ArtifactDescriptorView
    eligibility: EligibilityEvidence
