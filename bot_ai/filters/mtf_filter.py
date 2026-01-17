# ============================================
# ⏱️ mtf_filter.py — Мульти-таймфрейм фильтр
# --------------------------------------------
# Функция:
# - Проверяет тренд на старшем таймфрейме
# - Поддерживает SMA, EMA, ADX, RSI
# - Возвращает True/False для входа
# Зависимости: pandas, ta
# ============================================

import pandas as pd
import ta

def mtf_filter(higher_tf_df: pd.DataFrame, method: str = "sma", period: int = 50, direction: str = "long") -> bool:
    """
    Мульти-таймфрейм фильтр

    Параметры:
    - higher_tf_df: DataFrame старшего ТФ с колонкой 'close'
    - method: тип фильтра ('sma', 'ema', 'adx', 'rsi')
    - period: период индикатора
    - direction: 'long' или 'short'

    Возвращает:
    - True, если фильтр разрешает вход
    """
    if higher_tf_df is None or higher_tf_df.empty:
        return False

    close = higher_tf_df["close"]

    if method == "sma":
        ma = close.rolling(window=period).mean()
        if direction == "long":
            return close.iloc[-1] > ma.iloc[-1]
        else:
            return close.iloc[-1] < ma.iloc[-1]

    elif method == "ema":
        ema = close.ewm(span=period, adjust=False).mean()
        if direction == "long":
            return close.iloc[-1] > ema.iloc[-1]
        else:
            return close.iloc[-1] < ema.iloc[-1]

    elif method == "adx":
        adx = ta.trend.ADXIndicator(
            high=higher_tf_df["high"],
            low=higher_tf_df["low"],
            close=close,
            window=period
        ).adx()
        return adx.iloc[-1] > 20  # Порог можно вынести в параметры

    elif method == "rsi":
        rsi = ta.momentum.RSIIndicator(close=close, window=period).rsi()
        if direction == "long":
            return rsi.iloc[-1] > 50
        else:
            return rsi.iloc[-1] < 50

    return False
