# ============================================
# File: bot_ai/selector/fetch_and_filter_pairs.py
# Назначение: Отбор и фильтрация пар + безопасная запись whitelist
# ============================================

import json
import logging
import os

import ccxt

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def _whitelist_path() -> str:
    """Возвращает путь к whitelist.json (можно переопределить через переменную окружения)."""
    return os.getenv("WHITELIST_PATH", os.path.join("data", "whitelist.json"))

def save_whitelist(pairs):
    """Сохраняет список пар в whitelist.json."""
    cache_path = _whitelist_path()
    os.makedirs(os.path.dirname(cache_path), exist_ok=True)
    with open(cache_path, "w", encoding="utf-8") as f:
        json.dump(pairs, f, ensure_ascii=False, indent=2)
    logger.debug(f"[FETCH] whitelist.json записан: {cache_path}")
    return cache_path

def fetch_and_filter_pairs(cfg, use_cache=True, cache_ttl_hours=24):
    """Загружает пары с биржи и фильтрует по цене, объёму и волатильности."""
    logger.debug("[FETCH] старт отбора пар")
    cache_path = _whitelist_path()

    if use_cache and os.path.exists(cache_path):
        try:
            with open(cache_path, encoding="utf-8") as f:
                pairs = json.load(f)
                logger.info(
                    f"[FETCH] Загружено {
                        len(pairs)} пар из кеша {cache_path}")
                return pairs
        except Exception as e:
            logger.warning(f"[FETCH] Ошибка чтения кеша {cache_path}: {e}")

    try:
        ex_class = getattr(ccxt, cfg.exchange)
        ex = ex_class()
        markets = ex.load_markets()
        usdt_pairs = [p for p in markets if p.endswith(
            "/USDT") and markets[p].get("active")]

        filtered = []
        min_price = cfg.risk.get("min_price_usdt", 1)
        min_volume = cfg.risk.get("min_24h_volume_usdt", 100000)
        min_volatility = 0.005  # (high - low) / close

        for p in usdt_pairs:
            m = markets[p]
            try:
                price = float(m.get("info", {}).get("last", m.get("last", 0)))
                volume = float(m.get("quoteVolume", 0))
                if price < min_price or volume < min_volume:
                    continue

                high = float(m.get("high", 0))
                low = float(m.get("low", 0))
                close = float(m.get("close", price))
                if close == 0 or high == 0 or low == 0:
                    continue

                volatility = (high - low) / close
                if volatility < min_volatility:
                    continue

                filtered.append(p)
            except Exception as e:
                logger.debug(f"[FILTER] Ошибка при фильтрации пары {p}: {e}")

        logger.info(f"[FILTER] Отобрано {len(filtered)} пар после фильтрации")
        save_whitelist(filtered)
        return filtered

    except Exception as e:
        logger.error(f"[FETCH] Ошибка при загрузке рынков: {e}")
        return []

