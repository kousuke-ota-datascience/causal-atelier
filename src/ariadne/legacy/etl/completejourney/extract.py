"""Extract Complete Journey tables from RData files."""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Mapping

import rdata


DEFAULT_TABLE_TYPES: dict[str, str] = {
    "campaign_descriptions": "rda",
    "campaigns": "rda",
    "coupon_redemptions": "rda",
    "coupons": "rda",
    "demographics": "rda",
    "products": "rda",
    "transactions": "rds",
    "promotions": "rds",
}


class RDataLoadError(ValueError):
    """Raised when an unsupported RData file type is requested."""


class RDataLoadStrategy(ABC):
    """Strategy for one RData serialization format."""

    @abstractmethod
    def load(self, path: Path, logical_name: str) -> Any:
        """Load one logical table."""


class RdaLoadStrategy(RDataLoadStrategy):
    """Load a named object from an RDA container."""

    def load(self, path: Path, logical_name: str) -> Any:
        converted = rdata.conversion.convert(rdata.parser.parse_file(path))
        return converted[logical_name]


class RdsLoadStrategy(RDataLoadStrategy):
    """Load the sole object stored in an RDS file."""

    def load(self, path: Path, logical_name: str) -> Any:
        del logical_name
        return rdata.conversion.convert(rdata.parser.parse_file(path))


class RDataLoader:
    """Load a table using a configured RData strategy."""

    def __init__(self, strategy: RDataLoadStrategy) -> None:
        self._strategy = strategy

    def load(self, file_path: Path, logical_name: str) -> Any:
        return self._strategy.load(file_path, logical_name)


def build_rdata_loader(file_type: str) -> RDataLoader:
    """Return an RDA or RDS loader."""

    if file_type == "rda":
        return RDataLoader(RdaLoadStrategy())
    if file_type == "rds":
        return RDataLoader(RdsLoadStrategy())
    raise RDataLoadError(f"file type must be rda or rds: {file_type}")


class CompleteJourneyExtractor:
    """Extract configured Complete Journey tables from the repository data tree."""

    def __init__(self, project_root: Path | None = None) -> None:
        self.project_root = (project_root or Path.cwd()).resolve()
        self.raw_dir = self.project_root / "data/00_raw/completejourney/rdata"

    def build_file_path(self, logical_name: str, file_type: str) -> Path:
        return self.raw_dir / f"{logical_name}.{file_type}"

    def extract_all(
        self,
        table_types: Mapping[str, str] = DEFAULT_TABLE_TYPES,
    ) -> dict[str, Any]:
        """Extract all configured tables keyed by logical name."""

        return {
            name: build_rdata_loader(file_type).load(
                self.build_file_path(name, file_type),
                name,
            )
            for name, file_type in table_types.items()
        }


# Backward-compatible alias for the class name used by the initial prototype.
ExecuteRDataLoader = CompleteJourneyExtractor


__all__ = [
    "CompleteJourneyExtractor",
    "DEFAULT_TABLE_TYPES",
    "ExecuteRDataLoader",
    "RDataLoadError",
    "RDataLoader",
    "build_rdata_loader",
]
