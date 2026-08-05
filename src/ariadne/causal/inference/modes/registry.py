"""mode strategy の registry。"""

from __future__ import annotations

from .base import AnalysisModeStrategy
from .edge_weight_mode import EdgeWeightModeStrategy
from .treatment_effect_mode import TreatmentEffectModeStrategy


MODE_STRATEGIES: tuple[type[AnalysisModeStrategy], ...] = (
    EdgeWeightModeStrategy,
    TreatmentEffectModeStrategy,
)
MODE_STRATEGY_BY_NAME = {strategy.mode: strategy for strategy in MODE_STRATEGIES}
