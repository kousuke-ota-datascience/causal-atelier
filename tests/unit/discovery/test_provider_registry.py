"""Tests for DiscoveryInputProviderRegistry."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock

import pytest

from ariadne.application.discovery.providers.registry import DiscoveryInputProviderRegistry


class TestDiscoveryInputProviderRegistry:
    def _make_registry(self) -> DiscoveryInputProviderRegistry:
        registry = DiscoveryInputProviderRegistry()
        registry.register("completejourney", lambda req: MagicMock())
        registry.register("single_table", lambda req: MagicMock())
        return registry

    def test_create_registered_provider(self) -> None:
        registry = self._make_registry()
        provider = registry.create("completejourney", MagicMock())
        assert provider is not None

    def test_create_unknown_provider_raises(self) -> None:
        registry = self._make_registry()
        with pytest.raises(ValueError, match="Unknown input provider"):
            registry.create("nonexistent_provider", MagicMock())

    def test_registered_types_sorted(self) -> None:
        registry = self._make_registry()
        types = registry.registered_types()
        assert types == sorted(types)
        assert "completejourney" in types
        assert "single_table" in types

    def test_register_overwrites_existing(self) -> None:
        registry = DiscoveryInputProviderRegistry()
        sentinel_a = MagicMock(name="a")
        sentinel_b = MagicMock(name="b")
        registry.register("p", lambda req: sentinel_a)
        registry.register("p", lambda req: sentinel_b)
        provider = registry.create("p", MagicMock())
        assert provider is sentinel_b

    def test_error_message_lists_allowed_providers(self) -> None:
        registry = self._make_registry()
        with pytest.raises(ValueError) as exc_info:
            registry.create("arbitrary_dynamic_import", MagicMock())
        assert "completejourney" in str(exc_info.value)
        assert "single_table" in str(exc_info.value)

    def test_no_dynamic_import_of_user_provided_class(self) -> None:
        """Registry must refuse to resolve unknown keys, not dynamic-import them."""
        registry = self._make_registry()
        # A class path that would be dangerous to dynamic-import
        with pytest.raises(ValueError):
            registry.create("ariadne.evil.module.EvilClass", MagicMock())
