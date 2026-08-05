"""Dataset catalog application service."""

from ariadne.application.run_execution.services import _DataCatalogService


class DataCatalogService(_DataCatalogService):
    """Register immutable dataset versions and their profiling work."""

__all__ = ["DataCatalogService"]
