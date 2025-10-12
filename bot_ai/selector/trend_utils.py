# ============================================
# File: bot_ai/selector/trend_utils.py
# Назначение: функции для анализа тренда (SMA)
# ============================================

import statistics
import logging

logger = logging.getLogger(__name__)

def trend_ok(exchange=None, symbol=None, timeframe=None, sma_fast=1, sma_slow=2, **kwargs):
    """
    Проверка тренда через SMA.
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
