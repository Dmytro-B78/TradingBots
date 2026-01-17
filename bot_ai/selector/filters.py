# ============================================
# File: bot_ai/selector/filters.py
# Назначение: Расширенные фильтры для отбора пар
# ============================================

import logging

from .trend_utils import trend_ok as _trend_ok

logger = logging.getLogger(__name__)

def spread_ok(ticker, max_spread_pct, skip=False):
    """Проверка, что спред не превышает допустимый процент."""
    if skip:
        return True
    try:
        bid, ask = ticker.get("bid", 0), ticker.get("ask", 0)
        if not bid:
            return False
        spread_pct = (ask - bid) / bid * 100
        return spread_pct <= max_spread_pct
    except Exception:
        return False

def volume_ok(ticker, min_volume, skip=False):
    """Проверка, что объём торгов выше минимального порога."""
    if skip:
        return True
    try:
        return ticker.get("quoteVolume", 0) >= min_volume
    except Exception:
        return False

def price_ok(ticker, min_price=1.0, skip=False):
    """Проверка, что цена актива выше минимальной."""
    if skip:
        return True
    try:
        return float(ticker.get("last", 0)) >= min_price
    except Exception:
        return False

def volatility_ok(ticker, min_volatility=0.005, skip=False):
    """Проверка, что волатильность достаточная (на основе high-low/close)."""
    if skip:
        return True
    try:
        high = float(ticker.get("high", 0))
        low = float(ticker.get("low", 0))
        close = float(ticker.get("close", 0))
        if close == 0:
            return False
        return (high - low) / close >= min_volatility
    except Exception:
        return False

def riskguard_ok(risk_guard, symbol, skip=False):
    """Проверка RiskGuard на допустимость открытия сделки по инструменту."""
    if skip or not risk_guard:
        return True
    try:
        return risk_guard.can_open_trade(symbol)
    except Exception:
        return False

def trend_ok(exchange, symbol, tf, fast, slow, skip=False):
    """Проверка тренда по SMA (быстрая > медленной)."""
    if skip:
        return True
    try:
        return _trend_ok(exchange, symbol, tf=tf, fast=fast, slow=slow)
    except Exception:
        return False

