"""
Классификатор рыночного режима на основе скользящих средних и волатильности.
"""

import pandas as pd

def classify_market_regime(prices: list[float]) -> str:
    """
    Классифицирует рыночный режим по двум критериям:
    - Тренд: |SMA(20) - SMA(50)| / цена > 1% → "trend", иначе "flat"
    - Волатильность: std(доходностей за 20 периодов) > 2% → "high_vol", иначе "low_vol"

    :param prices: список цен (минимум 60 значений)
    :return: строка вида "trend_high_vol", "flat_low_vol", либо "unknown"
    """
    if len(prices) < 60:
        return "unknown"

    series = pd.Series(prices)
    returns = series.pct_change().dropna()

    sma_fast = series.rolling(20).mean()
    sma_slow = series.rolling(50).mean()
    trend_strength = abs(sma_fast - sma_slow).iloc[-1] / series.iloc[-1]

    volatility = returns.rolling(20).std().iloc[-1]

    trend = "trend" if trend_strength > 0.01 else "flat"
    vol = "high_vol" if volatility > 0.02 else "low_vol"

    return f"{trend}_{vol}"
