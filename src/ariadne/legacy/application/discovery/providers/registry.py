"""Provider registry for DiscoveryInputProvider."""

from __future__ import annotations

from typing import Any, Callable

from ariadne.application.discovery.ports import DiscoveryInputProvider

# Factory callable: (request) -> DiscoveryInputProvider
DiscoveryInputProviderFactory = Callable[..., DiscoveryInputProvider]


class DiscoveryInputProviderRegistry:
    """Allowlist-based registry for DiscoveryInputProvider implementations.

    Providers are registered by key and resolved on demand.  Unknown provider
    keys raise ``ValueError`` rather than attempting a dynamic import.

    Args:
        factories: Optional initial mapping of provider_type to factory callable.
    """

    def __init__(
        self,
        factories: dict[str, DiscoveryInputProviderFactory] | None = None,
    ) -> None:
        self._factories: dict[str, DiscoveryInputProviderFactory] = dict(factories or {})

    def register(
        self,
        provider_type: str,
        factory: DiscoveryInputProviderFactory,
    ) -> None:
        """Register a provider factory under a key.

        Args:
            provider_type: Unique string key (e.g. ``"completejourney"``).
            factory: Callable that accepts ``request`` and returns a provider.
        """
        self._factories[provider_type] = factory

    def create(
        self,
        provider_type: str,
        request: Any,
    ) -> DiscoveryInputProvider:
        """Resolve and instantiate a provider.

        Args:
            provider_type: Registered provider key.
            request: DiscoveryRequest passed to the factory.

        Returns:
            Configured DiscoveryInputProvider instance.

        Raises:
            ValueError: If ``provider_type`` is not registered.
        """
        if provider_type not in self._factories:
            allowed = sorted(self._factories)
            raise ValueError(
                f"Unknown input provider: {provider_type!r}. "
                f"Registered providers: {allowed}"
            )
        return self._factories[provider_type](request)

    def registered_types(self) -> list[str]:
        """Return sorted list of registered provider type keys."""
        return sorted(self._factories)


__all__ = ["DiscoveryInputProviderFactory", "DiscoveryInputProviderRegistry"]
