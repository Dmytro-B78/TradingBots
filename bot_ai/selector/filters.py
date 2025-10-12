# ============================================
# File: bot_ai/selector/filters.py
# ============================================

import logging
from .trend_utils import trend_ok as _trend_ok

logger = logging.getLogger(__name__)

def spread_ok(ticker, max_spread_pct, skip=False):
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
    if skip:
        return True
    try:
        return ticker.get("quoteVolume", 0) >= min_volume
    except Exception:
        return False

def riskguard_ok(risk_guard, symbol, skip=False):
    if skip or not risk_guard:
        return True
    try:
        return risk_guard.can_open_trade(symbol)
    except Exception:
        return False

def trend_ok(exchange, symbol, tf, fast, slow, skip=False):
    if skip:
        return True
    try:
        return _trend_ok(exchange, symbol, tf=tf, fast=fast, slow=slow)
    except Exception:
        return False
