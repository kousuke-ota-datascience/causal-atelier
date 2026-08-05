"""pipeline mode の strategy interface。"""

from __future__ import annotations

from abc import ABC, abstractmethod

from ..context import RunContext


class AnalysisModeStrategy(ABC):
    """実行可能な pipeline mode の抽象 base class。"""

    mode: str

    @abstractmethod
    def run(self, context: RunContext) -> None:
        """analysis mode を実行する。

        Args:
            context: Resolved run context containing configuration and paths.

        Raises:
            ValueError: If the mode configuration is invalid.
        """
        raise NotImplementedError
