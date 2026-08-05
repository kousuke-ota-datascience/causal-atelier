"""Provider package for DiscoveryInputProvider implementations."""

from ariadne.application.discovery.providers.completejourney import (
    CompleteJourneyDiscoveryInputProvider,
)
from ariadne.application.discovery.providers.registry import (
    DiscoveryInputProviderFactory,
    DiscoveryInputProviderRegistry,
)
from ariadne.application.discovery.providers.single_table import (
    SingleTableDiscoveryInputProvider,
)

__all__ = [
    "CompleteJourneyDiscoveryInputProvider",
    "DiscoveryInputProviderFactory",
    "DiscoveryInputProviderRegistry",
    "SingleTableDiscoveryInputProvider",
]
