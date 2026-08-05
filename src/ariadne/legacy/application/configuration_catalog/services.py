"""Configuration catalog application service."""

from ariadne.application.run_execution.services import _ConfigurationService


class ConfigurationService(_ConfigurationService):
    """Create, validate, project, and publish configuration versions."""

__all__ = ["ConfigurationService"]
