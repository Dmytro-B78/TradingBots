import ccxt
import logging
import json
import os
import time
import pandas as pd

def fetch_and_filter_pairs(cfg, risk_guard=None, use_cache=True, cache_ttl_hours=24, show_top_n=5):
    logger = logging.getLogger(__name__)
    cache_file = 'data/whitelist.json'

    # --- Чтение кэша ---
    if use_cache and os.path.exists(cache_file):
        file_age_hours = (time.time() - os.path.getmtime(cache_file)) / 3600
        if file_age_hours < cache_ttl_hours:
            logger.info(f"Загрузка whitelist из {cache_file} (возраст {file_age_hours:.1f} ч.)")
            with open(cache_file, 'r', encoding='utf-8') as f:
                pairs = json.load(f)
            show_top_pairs(cfg, pairs, top_n=show_top_n)
            return pairs
        else:
            logger.info(f"Whitelist устарел ({file_age_hours:.1f} ч.), обновляем...")

    # --- Загрузка рынков ---
    exchange_class = getattr(ccxt, cfg.exchange)
    exchange = exchange_class({'enableRateLimit': True})

    logger.info(f"Загрузка списка рынков с {cfg.exchange}...")
    markets = exchange.load_markets()
    usdt_pairs = [s for s in markets if s.endswith('/USDT') and markets[s]['active']]

    logger.info(f"Найдено {len(usdt_pairs)} USDT-пар")

    filtered = []
    for symbol in usdt_pairs:
        try:
            # --- Проверка RiskGuard ---
            if risk_guard and not risk_guard.can_open_trade(symbol):
                logger.debug(f"{symbol} пропущен: cooldown или лимит RiskGuard")
                continue

            ticker = exchange.fetch_ticker(symbol)
            volume_usdt = ticker.get('quoteVolume', 0)
            ask = ticker.get('ask')
            bid = ticker.get('bid')
            spread_pct = ((ask - bid) / bid) * 100 if bid and ask else 999

            # --- Фильтр по объёму ---
            if volume_usdt < cfg.risk.min_24h_volume_usdt:
                logger.debug(f"{symbol} пропущен: объём {volume_usdt} < {cfg.risk.min_24h_volume_usdt}")
                continue

            # --- Фильтр по спреду ---
            if spread_pct > cfg.risk.max_spread_pct:
                logger.debug(f"{symbol} пропущен: спред {spread_pct:.2f}% > {cfg.risk.max_spread_pct}%")
                continue

            # --- Фильтр по тренду D1 ---
            if not _trend_ok(exchange, symbol,
                             tf=cfg.pair_selection.get("d1_timeframe", "1d"),
                             fast=cfg.pair_selection.get("d1_sma_fast", 50),
                             slow=cfg.pair_selection.get("d1_sma_slow", 200)):
                logger.debug(f"{symbol} пропущен: тренд D1 не восходящий")
                continue

            # --- Фильтр по тренду LTF ---
            if not _trend_ok(exchange, symbol,
                             tf=cfg.pair_selection.get("ltf_timeframe", "1h"),
                             fast=cfg.pair_selection.get("ltf_sma_fast", 20),
                             slow=cfg.pair_selection.get("ltf_sma_slow", 50)):
                logger.debug(f"{symbol} пропущен: тренд LTF не восходящий")
                continue

            filtered.append(symbol)

        except Exception as e:
            logger.warning(f"Ошибка при обработке {symbol}: {e}")

    logger.info(f"Отобрано {len(filtered)} пар после фильтров")

    # --- Сохраняем whitelist ---
    os.makedirs('data', exist_ok=True)
    with open(cache_file, 'w', encoding='utf-8') as f:
        json.dump(filtered, f, ensure_ascii=False, indent=2)

    logger.info(f"Whitelist сохранён в {cache_file}")

    # --- Показать топ N ---
    show_top_pairs(cfg, filtered, top_n=show_top_n)

    return filtered

def _trend_ok(exchange, symbol, tf, fast, slow):
    try:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe=tf, limit=max(fast, slow))
        df = pd.DataFrame(ohlcv, columns=["time", "open", "high", "low", "close", "volume"])
        sma_fast = df["close"].rolling(window=fast).mean().iloc[-1]
        sma_slow = df["close"].rolling(window=slow).mean().iloc[-1]
        return sma_fast > sma_slow
    except Exception:
        return False

def show_top_pairs(cfg, pairs, top_n=5):
    logger = logging.getLogger(__name__)
    if not pairs:
        logger.info("Whitelist пуст.")
        return

    exchange_class = getattr(ccxt, cfg.exchange)
    exchange = exchange_class({'enableRateLimit': True})

    volumes = []
    for symbol in pairs:
        try:
            ticker = exchange.fetch_ticker(symbol)
            volumes.append((symbol, ticker.get('quoteVolume', 0)))
        except Exception:
            pass

    volumes.sort(key=lambda x: x[1], reverse=True)
    top_pairs = volumes[:top_n]

    logger.info(f"Топ-{top_n} пар по объёму (USDT):")
    for sym, vol in top_pairs:
        logger.info(f"{sym}: {vol:,.0f} USDT")

def select_pairs(cfg, risk_guard=None):
    """
    Основная точка входа для main.py.
    Возвращает список отобранных пар.
    """
    return fetch_and_filter_pairs(cfg, risk_guard=risk_guard)
