# bot_ai/filters/trend_filter.py
# 📈 Фильтр тренда: исключает периоды со слабым трендом по индексу ADX

import pandas as pd
import pandas_ta as ta

class TrendFilter:
    def __init__(self, adx_window: int = 14, adx_threshold: float = 20):
        """
        :param adx_window: окно ADX
        :param adx_threshold: минимальное значение ADX для допуска к сделке
        """
        self.adx_window = adx_window
        self.adx_threshold = adx_threshold

    def apply(self, df: pd.DataFrame) -> pd.Series:
        """
        Возвращает булеву серию: True — свеча проходит фильтр тренда.
        """
        if not {"high", "low", "close"}.issubset(df.columns):
            raise ValueError("DataFrame должен содержать колонки: high, low, close")

        adx = ta.adx(high=df["high"], low=df["low"], close=df["close"], length=self.adx_window)["ADX_" + str(self.adx_window)]
        return adx > self.adx_threshold
