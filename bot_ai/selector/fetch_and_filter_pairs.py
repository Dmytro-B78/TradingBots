# ============================================
# File: bot_ai/selector/fetch_and_filter_pairs.py
# Purpose: Отбор и фильтрация пар + безопасная запись whitelist
# ============================================

import os
import json
import logging
import ccxt

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def _whitelist_path() -> str:
    """
    Возвращает целевой путь для whitelist, приоритет — переменная окружения WHITELIST_PATH.
    """
    return os.getenv("WHITELIST_PATH", os.path.join("data", "whitelist.json"))

def save_whitelist(pairs):
    """
    Безопасно сохраняет список пар напрямую в целевой whitelist.json.
    Исключаем любые копирования/перемещения: пишем сразу в _whitelist_path().
    """
    cache_path = _whitelist_path()
    os.makedirs(os.path.dirname(cache_path), exist_ok=True)
    with open(cache_path, "w", encoding="utf-8") as f:
        json.dump(pairs, f, ensure_ascii=False, indent=2)
    logger.debug(f"[FETCH] whitelist.json записан: {cache_path}")
    return cache_path

def fetch_and_filter_pairs(cfg, use_cache=True, cache_ttl_hours=24):
    """
    Минимальная рабочая логика отбора пар:
    - При use_cache загружает whitelist из _whitelist_path(), если доступно
    - Иначе загружает рынки у cfg.exchange и сохраняет whitelist
    """
    logger.debug("[FETCH] старт отбора пар")
    cache_path = _whitelist_path()

    if use_cache and os.path.exists(cache_path):
        try:
            with open(cache_path, encoding="utf-8") as f:
                pairs = json.load(f)
                logger.info(f"[FETCH] Загружено {len(pairs)} пар из кеша {cache_path}")
                return pairs
        except Exception as e:
            logger.warning(f"[FETCH] Ошибка чтения кеша {cache_path}: {e}")

    try:
        ex_class = getattr(ccxt, cfg.exchange)
        ex = ex_class()
        markets = ex.load_markets()
        usdt_pairs = [p for p in markets if p.endswith("/USDT") and markets[p].get("active")]
        logger.info(f"[FETCH] Всего активных USDT-пар: {len(usdt_pairs)}")
        save_whitelist(usdt_pairs)
        return usdt_pairs
    except Exception as e:
        logger.error(f"[FETCH] Ошибка при загрузке рынков: {e}")
        return []
