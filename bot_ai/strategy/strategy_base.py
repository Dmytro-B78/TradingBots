# ============================================
# File: bot_ai/strategy/strategy_base.py
# Purpose: Abstract base class for all strategies
# Format: UTF-8 without BOM
# Compatible with: strategy loader, adaptive engine
# ============================================

from abc import ABC, abstractmethod
import pandas as pd
from bot_ai.core.signal import Signal

class StrategyBase(ABC):
    def __init__(self, config: dict):
        self.config = config

    @abstractmethod
    def generate_signal(self, df: pd.DataFrame) -> Signal | None:
        pass
