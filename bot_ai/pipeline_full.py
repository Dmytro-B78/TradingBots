# ============================================
# File: bot_ai/pipeline_full.py
# ============================================

import os
import json
import logging
import statistics

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def _whitelist_path():
    return os.getenv("WHITELIST_PATH", os.path.join("data", "whitelist.json"))

def save_whitelist(pairs):
    path = _whitelist_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(pairs, f, ensure_ascii=False, indent=2)
    return path

def _trend_ok(exchange, symbol, timeframe, sma_fast, sma_slow):
    try:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, sma_slow)
        closes = [c[4] for c in ohlcv]
        if len(closes) < sma_slow:
            return False
        slow = statistics.mean(closes[-sma_slow:])
        fast = statistics.mean(closes[-sma_fast:])
        return fast > slow
    except Exception:
        return False

def run_full_pipeline(cfg, **kwargs):
    save_whitelist(["BTC/USDT", "ETH/USDT"])
    return True
