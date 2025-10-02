import os
import time
import json
import logging
import ccxt
import pandas as pd
import sys

# --- Настройка логгера на UTF‑8 ---
logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s %(name)s:%(filename)s:%(lineno)d %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

def _trend_ok(exchange, symbol, tf, fast, slow):
    """Проверка тренда по SMA с выводом размера датасета и последних значений."""
    try:
        limit = max(fast, slow)
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe=tf, limit=limit)
        closes = [c[4] for c in ohlcv]
        sma_fast = pd.Series(closes).rolling(window=fast).mean().iloc[-1]
        sma_slow = pd.Series(closes).rolling(window=slow).mean().iloc[-1]
        logging.getLogger(__name__).debug(
            f"[TREND] {symbol} {tf}: {len(closes)} свечей, SMA_fast={sma_fast}, SMA_slow={sma_slow}"
        )
        return bool(sma_fast > sma_slow)
    except Exception as e:
        logging.getLogger(__name__).warning(f"[TREND] {symbol} {tf} ERROR={e}")
        return False

def show_top_pairs(cfg, pairs, top_n=5):
    """Вывод топ-N пар по объёму."""
    logger = logging.getLogger(__name__)
    if not pairs:
        logger.info("Whitelist пуст.")
        return
    try:
        ex_class = getattr(ccxt, cfg.exchange)
        ex = ex_class()
        volumes = []
        for p in pairs:
            try:
                ticker = ex.fetch_ticker(p)
                volumes.append((p, ticker.get("quoteVolume", 0)))
            except Exception as e:
                logger.warning(f"[ERROR] {p}: {e}")
        volumes.sort(key=lambda x: x[1], reverse=True)
        logger.info(f"Топ-{top_n} пар по объёму (USDT):")
        for p, vol in volumes[:top_n]:
            try:
                vol_int = int(vol)
            except (ValueError, TypeError):
                vol_int = vol
            logger.info(f"{p}: {vol_int} USDT")
    except Exception as e:
        logger.error(f"Ошибка show_top_pairs: {e}")

def fetch_and_filter_pairs(
    cfg,
    risk_guard=None,
    use_cache=True,
    cache_ttl_hours=24,
    skip_riskguard_for=None,
    skip_volume_for=None,
    skip_spread_for=None,
    skip_trend_d1_for=None,
    skip_trend_ltf_for=None
):
    """Основная логика отбора пар с расширенным логом и фильтром отсутствующих пар."""
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger.debug("[PIPELINE] старт фильтрации")

    skip_riskguard_for = skip_riskguard_for or []
    skip_volume_for = skip_volume_for or []
    skip_spread_for = skip_spread_for or []
    skip_trend_d1_for = skip_trend_d1_for or []
    skip_trend_ltf_for = skip_trend_ltf_for or []

    cache_path = os.path.join("data", "whitelist.json")
    if use_cache and os.path.exists(cache_path):
        age_hours = (time.time() - os.path.getmtime(cache_path)) / 3600
        if age_hours <= cache_ttl_hours:
            with open(cache_path, encoding="utf-8") as f:
                pairs = json.load(f)
            show_top_pairs(cfg, pairs)
            return pairs

    ex_class = getattr(ccxt, cfg.exchange)
    ex = ex_class()
    markets = ex.load_markets()
    usdt_pairs = [p for p in markets if p.endswith("/USDT") and markets[p].get("active")]
    logger.info(f"[PIPELINE] Всего активных USDT-пар: {len(usdt_pairs)}")

    filtered = []
    for symbol in usdt_pairs:
        try:
            if symbol not in markets:
                logger.debug(f"[FILTER] {symbol}: отсутствует на бирже")
                continue

            if risk_guard and symbol not in skip_riskguard_for and not risk_guard.can_open_trade(symbol):
                logger.debug(f"[FILTER] {symbol}: отсеян RiskGuard")
                continue

            ticker = ex.fetch_ticker(symbol)
            vol = ticker.get("quoteVolume", 0)
            if symbol not in skip_volume_for and vol < cfg.risk.min_24h_volume_usdt:
                logger.debug(f"[FILTER] {symbol}: объём {vol} < {cfg.risk.min_24h_volume_usdt}")
                continue

            ask = ticker.get("ask", 0)
            bid = ticker.get("bid", 0)
            spread_pct = ((ask - bid) / ask) * 100 if ask else 0
            if symbol not in skip_spread_for and spread_pct > cfg.risk.max_spread_pct:
                logger.debug(f"[FILTER] {symbol}: спред {spread_pct:.2f}% > {cfg.risk.max_spread_pct}")
                continue

            if symbol not in skip_trend_d1_for and not _trend_ok(
                ex, symbol,
                cfg.pair_selection["d1_timeframe"],
                cfg.pair_selection["d1_sma_fast"],
                cfg.pair_selection["d1_sma_slow"]
            ):
                logger.debug(f"[FILTER] {symbol}: тренд D1 не проходит")
                continue

            if symbol not in skip_trend_ltf_for and not _trend_ok(
                ex, symbol,
                cfg.pair_selection["ltf_timeframe"],
                cfg.pair_selection["ltf_sma_fast"],
                cfg.pair_selection["ltf_sma_slow"]
            ):
                logger.debug(f"[FILTER] {symbol}: тренд LTF не проходит")
                continue

            logger.debug(f"[PASS] {symbol}: прошла все фильтры")
            filtered.append(symbol)

        except Exception as e:
            logger.warning(f"[ERROR] {symbol}: {e}")

    logger.info(f"[PIPELINE] Выбрано {len(filtered)} пар: {filtered}")
    return filtered

def select_pairs(cfg, risk_guard=None, **kwargs):
    """Точка входа для отбора пар."""
    return fetch_and_filter_pairs(cfg, risk_guard=risk_guard, **kwargs)
