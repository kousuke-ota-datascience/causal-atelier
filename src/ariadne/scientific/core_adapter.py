"""ScientificCoreAdapter – unified entry point for the product domain's ScientificCorePort."""

from __future__ import annotations

from pathlib import Path

from ariadne.product.ports.scientific_core import (
    DiscoveryInput,
    IdentificationInput,
    EstimationInput,
    RefutationInput,
    SensitivityInput,
    ScientificResultDescriptor,
)
from ariadne.scientific.discovery.adapter import DiscoveryAdapter
from ariadne.scientific.inference.adapter import EstimationAdapter
from ariadne.scientific.identification.adapter import IdentificationAdapter
from ariadne.scientific.refutation.adapter import RefutationAdapter
from ariadne.scientific.sensitivity.adapter import SensitivityAdapter


class ScientificCoreAdapter:
    """Implements ScientificCorePort by delegating to discovery and inference adapters."""

    def __init__(self) -> None:
        self._discovery = DiscoveryAdapter()
        self._estimation = EstimationAdapter()
        self._identification = IdentificationAdapter()
        self._refutation = RefutationAdapter()
        self._sensitivity = SensitivityAdapter()

    def run_discovery(self, input_: DiscoveryInput, output_dir: Path) -> list[ScientificResultDescriptor]:
        return self._discovery.run(input_, output_dir)

    def run_identification(self, input_: IdentificationInput, output_dir: Path) -> list[ScientificResultDescriptor]:
        return self._identification.run(input_, output_dir)

    def run_estimation(self, input_: EstimationInput, output_dir: Path) -> list[ScientificResultDescriptor]:
        return self._estimation.run(input_, output_dir)

    def run_refutation(self, input_: RefutationInput, output_dir: Path) -> list[ScientificResultDescriptor]:
        return self._refutation.run(input_, output_dir)

    def run_sensitivity(self, input_: SensitivityInput, output_dir: Path) -> list[ScientificResultDescriptor]:
        return self._sensitivity.run(input_, output_dir)
