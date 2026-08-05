"""因果推論パイプラインが送出する custom exception。"""

from __future__ import annotations


class PipelineConfigError(ValueError):
    """Raised when pipeline configuration is missing or inconsistent."""
