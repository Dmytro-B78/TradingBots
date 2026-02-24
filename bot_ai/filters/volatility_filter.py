"""
Фильтр волатильности на основе индикатора ATR.
"""

import pandas as pd
import pandas_ta as ta

class VolatilityFilter:
    def __init__(self, atr_window: int = 14, atr_threshold: float = 0.005):
        """
        :param atr_window: окно ATR (по умолчанию 14)
        :param atr_threshold: порог волатильности (например, 0.005 = 0.5%)
        """
        self.atr_window = atr_window
        self.atr_threshold = atr_threshold

    def apply(self, df: pd.DataFrame) -> pd.Series:
        """
        Применяет фильтр волатильности. Возвращает булеву серию, где True — допустимая волатильность.
        Требуются колонки: high, low, close.
        """
        if not {"high", "low", "close"}.issubset(df.columns):
            raise ValueError("DataFrame должен содержать колонки: high, low, close")

        atr = ta.atr(high=df["high"], low=df["low"], close=df["close"], length=self.atr_window)
        atr_pct = atr / df["close"]
        return atr_pct > self.atr_threshold
