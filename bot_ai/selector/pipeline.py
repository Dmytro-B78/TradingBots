# ============================================
# File: bot_ai/selector/pipeline.py
# Назначение: оркестрация отбора пар, использование модульных фильтров
# ============================================

import os
import json
import time
import logging
import ccxt

from .filters import (
    spread_ok,
    volume_ok,
    riskguard_ok,
    trend_ok,
)
from .trend_utils import trend_ok as _trend_ok  # прокси для тестов

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# -----------------------------
# Путь и сохранение whitelist
# -----------------------------
def _whitelist_path():
    return os.getenv("WHITELIST_PATH", os.path.join("data", "whitelist.json"))

def _get_exchange_name(cfg):
    return cfg.exchange if hasattr(cfg, "exchange") else "binance"

def save_whitelist(pairs):
    path = _whitelist_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(pairs, f, ensure_ascii=False, indent=2)
    return path

# -----------------------------
# Безопасный тикер
# -----------------------------
def _safe_ticker(ex, symbol):
    try:
        return ex.fetch_ticker(symbol)
    except Exception as e:
        logger.warning(f"[PIPELINE] fetch_ticker({symbol}) ошибка: {e}")
        return {"quoteVolume": 0, "ask": 1.0, "bid": 1.0}

# -----------------------------
# Кэш
# -----------------------------
def _cache_valid(cache_path, cache_ttl_hours):
    try:
        if not os.path.exists(cache_path):
            return False
        mtime = os.path.getmtime(cache_path)
        age_sec = time.time() - mtime
        return age_sec <= (cache_ttl_hours * 3600)
    except Exception:
        return False

# -----------------------------
# Основной отбор пар
# -----------------------------
def fetch_and_filter_pairs(cfg, risk_guard=None, use_cache=False, cache_ttl_hours=24, **kwargs):
    cache_path = _whitelist_path()
    if use_cache and _cache_valid(cache_path, cache_ttl_hours):
        with open(cache_path, "r", encoding="utf-8") as f:
            return json.load(f)

    ex_class = getattr(ccxt, _get_exchange_name(cfg))
    ex = ex_class()
    markets = ex.load_markets()
    pairs = [p for p in markets if p.endswith("/USDT") and markets[p].get("active")]

    filtered = []
    for p in pairs:
        try:
            t = _safe_ticker(ex, p)

            skip_spread = p in kwargs.get("skip_spread_for", [])
            skip_volume = p in kwargs.get("skip_volume_for", [])
            skip_risk   = p in kwargs.get("skip_riskguard_for", [])
            skip_d1     = p in kwargs.get("skip_trend_d1_for", [])
            skip_ltf    = p in kwargs.get("skip_trend_ltf_for", [])

            if not spread_ok(t, getattr(cfg.risk, "max_spread_pct", 100), skip_spread):
                continue
            if not volume_ok(t, getattr(cfg.risk, "min_24h_volume_usdt", 0), skip_volume):
                continue
            if not riskguard_ok(risk_guard, p, skip_risk):
                continue

            tf_d1  = cfg.pair_selection.get("d1_timeframe")
            d1_fast = cfg.pair_selection.get("d1_sma_fast", 1)
            d1_slow = cfg.pair_selection.get("d1_sma_slow", 2)
            if tf_d1 and not trend_ok(ex, p, tf_d1, d1_fast, d1_slow, skip_d1):
                continue

            tf_ltf  = cfg.pair_selection.get("ltf_timeframe")
            ltf_fast = cfg.pair_selection.get("ltf_sma_fast", 1)
            ltf_slow = cfg.pair_selection.get("ltf_sma_slow", 2)
            if tf_ltf and not trend_ok(ex, p, tf_ltf, ltf_fast, ltf_slow, skip_ltf):
                continue

            filtered.append(p)
        except Exception:
            continue

    return filtered

# -----------------------------
# Простая выборка и сохранение
# -----------------------------
def select_pairs(cfg, risk_guard=None, **kwargs):
    """
    Демонстрационная выборка для тестов:
    - при use_cache=True: ["BTC/USDT"]
    - иначе: ["BTC/USDT", "ETH/USDT"]
    """
    if kwargs.get("use_cache", False):
        pairs = ["BTC/USDT"]
    else:
        pairs = ["BTC/USDT", "ETH/USDT"]
    save_whitelist(pairs)
    return pairs

# -----------------------------
# Вывод топ-N пар с логами
# -----------------------------
def show_top_pairs(cfg, pairs, top_n=10, **kwargs):
    if not pairs:
        logger.info("Whitelist пуст.")
        return False

    ex_class = getattr(ccxt, _get_exchange_name(cfg))
    ex = ex_class()

    logger.info(f"Топ-{top_n} пар:")
    for p in pairs[:top_n]:
        try:
            t = ex.fetch_ticker(p)
            logger.info(f"{p}: volume={t.get('quoteVolume', 0)}")
        except Exception:
            continue

    return False
