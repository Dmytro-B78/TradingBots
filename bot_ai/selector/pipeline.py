import ccxt
import logging
import json
import os
import time

def fetch_and_filter_pairs(cfg, use_cache=True, cache_ttl_hours=24, show_top_n=5):
    logger = logging.getLogger(__name__)
    cache_file = 'data/whitelist.json'

    # Проверка кэша
    if use_cache and os.path.exists(cache_file):
        file_age_hours = (time.time() - os.path.getmtime(cache_file)) / 3600
        if file_age_hours < cache_ttl_hours:
            logger.info(f"Загружаем whitelist из {cache_file} (возраст {file_age_hours:.1f} ч.)")
            with open(cache_file, 'r', encoding='utf-8') as f:
                pairs = json.load(f)
            show_top_pairs(cfg, pairs, top_n=show_top_n)
            return pairs
        else:
            logger.info(f"Whitelist устарел ({file_age_hours:.1f} ч.), обновляем...")

    # Загружаем с биржи
    exchange_class = getattr(ccxt, cfg.exchange)
    exchange = exchange_class({'enableRateLimit': True})

    logger.info(f"Загружаем список пар с {cfg.exchange}...")
    markets = exchange.load_markets()
    usdt_pairs = [s for s in markets if s.endswith('/USDT') and markets[s]['active']]

    logger.info(f"Всего найдено {len(usdt_pairs)} USDT-пар")

    filtered = []
    for symbol in usdt_pairs:
        try:
            ticker = exchange.fetch_ticker(symbol)
            volume_usdt = ticker.get('quoteVolume', 0)
            ask = ticker.get('ask')
            bid = ticker.get('bid')
            spread_pct = ((ask - bid) / bid) * 100 if bid and ask else 999

            if volume_usdt >= cfg.risk.min_24h_volume_usdt and spread_pct <= cfg.risk.max_spread_pct:
                filtered.append(symbol)
        except Exception as e:
            logger.warning(f"Ошибка при обработке {symbol}: {e}")

    logger.info(f"Отобрано {len(filtered)} пар после фильтров")

    # Сохраняем whitelist
    os.makedirs('data', exist_ok=True)
    with open(cache_file, 'w', encoding='utf-8') as f:
        json.dump(filtered, f, ensure_ascii=False, indent=2)

    logger.info(f"Whitelist сохранён в {cache_file}")

    # Покажем ТОП‑N по объёму
    show_top_pairs(cfg, filtered, top_n=show_top_n)

    return filtered

def show_top_pairs(cfg, pairs, top_n=5):
    logger = logging.getLogger(__name__)
    if not pairs:
        logger.info("Whitelist пуст — нечего показывать.")
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

    logger.info(f"ТОП-{top_n} пар по объёму (USDT):")
    for sym, vol in top_pairs:
        logger.info(f"{sym}: {vol:,.0f} USDT")