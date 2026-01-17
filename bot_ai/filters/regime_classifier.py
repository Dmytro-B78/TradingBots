# regime_classifier.py — классификация рыночного режима (тренд / флэт + волатильность)

import pandas as pd

def classify_market_regime(prices: list[float]) -> str:
    """
    Классифицирует рынок по двум осям:
    - Тренд: |SMA(20) - SMA(50)| > 1% → тренд, иначе флэт
    - Волатильность: std(доходностей) > 2% → высокая, иначе низкая

    Возвращает: "trend_high_vol", "flat_low_vol" и т.п.
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
