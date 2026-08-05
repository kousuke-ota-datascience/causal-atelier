"""ScientificCoreAdapter – unified entry point for the product domain's ScientificCorePort."""

from __future__ import annotations

from pathlib import Path

from ariadne.product.ports.scientific_core import (
    DiscoveryInput,
    DiscoveryOutput,
    EstimationInput,
    EstimationOutput,
)
from ariadne.scientific.discovery.adapter import DiscoveryAdapter
from ariadne.scientific.inference.adapter import EstimationAdapter


class ScientificCoreAdapter:
    """Implements ScientificCorePort by delegating to discovery and inference adapters."""

    def __init__(self) -> None:
        self._discovery = DiscoveryAdapter()
        self._estimation = EstimationAdapter()

    def run_discovery(self, input_: DiscoveryInput, output_dir: Path) -> DiscoveryOutput:
        return self._discovery.run(input_, output_dir)

    def run_estimation(self, input_: EstimationInput, output_dir: Path) -> EstimationOutput:
        return self._estimation.run(input_, output_dir)
