"""Causal design schema shared by runtime validation and inference."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping


class Estimand(str, Enum):
    """Supported target estimands."""

    ATE = "ATE"
    ATT = "ATT"


@dataclass(frozen=True)
class TreatmentSpec:
    """Treatment definition."""

    name: str
    time: str | None = None
    levels: tuple[Any, ...] = (0, 1)

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "TreatmentSpec":
        """Build a treatment spec from YAML."""

        return cls(
            name=str(value["name"]),
            time=None if value.get("time") is None else str(value["time"]),
            levels=tuple(value.get("levels", (0, 1))),
        )

    def to_dict(self) -> dict[str, Any]:
        """Serialize the treatment spec."""

        return {"name": self.name, "time": self.time, "levels": list(self.levels)}


@dataclass(frozen=True)
class OutcomeSpec:
    """Outcome definition."""

    name: str
    window: dict[str, Any] | None = None

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "OutcomeSpec":
        """Build an outcome spec from YAML."""

        return cls(
            name=str(value["name"]),
            window=None if value.get("window") is None else dict(value["window"]),
        )

    def to_dict(self) -> dict[str, Any]:
        """Serialize the outcome spec."""

        return {"name": self.name, "window": self.window}


@dataclass(frozen=True)
class CausalDesign:
    """Top-level causal design contract."""

    estimand: Estimand
    treatment: TreatmentSpec
    outcome: OutcomeSpec
    unit: str
    time_zero: str | None = None
    assumptions: tuple[str, ...] = ()
    adjustment_set: str | None = None

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "CausalDesign":
        """Build a causal design from YAML data."""

        data = dict(value.get("causal_design", value))
        if "estimand" not in data:
            raise ValueError("causal_design.estimand is required")
        return cls(
            estimand=Estimand(str(data["estimand"])),
            treatment=TreatmentSpec.from_mapping(dict(data["treatment"])),
            outcome=OutcomeSpec.from_mapping(dict(data["outcome"])),
            unit=str(data.get("unit", "household")),
            time_zero=None if data.get("time_zero") is None else str(data["time_zero"]),
            assumptions=tuple(str(item) for item in data.get("assumptions", ())),
            adjustment_set=None
            if data.get("adjustment_set") is None
            else str(data["adjustment_set"]),
        )

    def to_dict(self) -> dict[str, Any]:
        """Serialize the causal design."""

        return {
            "causal_design": {
                "estimand": self.estimand.value,
                "treatment": self.treatment.to_dict(),
                "outcome": self.outcome.to_dict(),
                "unit": self.unit,
                "time_zero": self.time_zero,
                "assumptions": list(self.assumptions),
                "adjustment_set": self.adjustment_set,
            }
        }


__all__ = ["CausalDesign", "Estimand", "OutcomeSpec", "TreatmentSpec"]
