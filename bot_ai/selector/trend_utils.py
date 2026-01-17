# ============================================
# File: bot_ai/selector/trend_utils.py
# Назначение: Расчёт тренда и определение рыночного режима
# ============================================

import logging
import statistics

logger = logging.getLogger(__name__)

def trend_ok(
        exchange=None,
        symbol=None,
        timeframe=None,
        sma_fast=1,
        sma_slow=2,
        **kwargs):
    """
    Проверка тренда через SMA: fast > slow.
    Поддерживает вызов: trend_ok(..., tf="1d", fast=1, slow=2)
    """
    if "tf" in kwargs:
        timeframe = kwargs["tf"]
    if "fast" in kwargs:
        sma_fast = kwargs["fast"]
    if "slow" in kwargs:
        sma_slow = kwargs["slow"]
    try:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, sma_slow)
        closes = [c[4] for c in ohlcv]
        if len(closes) < sma_slow:
            return False
        slow = statistics.mean(closes[-sma_slow:])
        fast = statistics.mean(closes[-sma_fast:])
        return fast > slow
    except Exception as e:
        logger.debug(f"[TREND] Ошибка при расчёте тренда {symbol}: {e}")
        return False

def detect_regime(
        exchange,
        symbol,
        tf="1d",
        sma_fast=50,
        sma_slow=200,
        bb_length=20,
        atr_length=14):
    """
    Определяет рыночный режим:
    - uptrend: SMA50 > SMA200
    - downtrend: SMA50 < SMA200
    - range: узкие BB и низкий ATR
    - volatile: высокая волатильность без тренда
    """
    try:
        import pandas as pd
        import pandas_ta as ta

        ohlcv = exchange.fetch_ohlcv(symbol, tf, limit=max(sma_slow + 10, 250))
        df = pd.DataFrame(
            ohlcv,
            columns=[
                "ts",
                "open",
                "high",
                "low",
                "close",
                "volume"])
        df["sma_fast"] = df["close"].rolling(sma_fast).mean()
        df["sma_slow"] = df["close"].rolling(sma_slow).mean()
        bb = ta.bbands(df["close"], length=bb_length)
        df["bb_width"] = bb["BBU_20_2.0"] - bb["BBL_20_2.0"]
        df["atr"] = ta.atr(
            df["high"],
            df["low"],
            df["close"],
            length=atr_length)

        latest = df.iloc[-1]
        if latest["sma_fast"] > latest["sma_slow"]:
            return "uptrend"
        elif latest["sma_fast"] < latest["sma_slow"]:
            return "downtrend"
        elif latest["bb_width"] / latest["close"] < 0.03 and latest["atr"] / latest["close"] < 0.01:
            return "range"
        else:
            return "volatile"
    except Exception as e:
        logger.debug(f"[REGIME] Ошибка при определении режима {symbol}: {e}")
        return "unknown"

