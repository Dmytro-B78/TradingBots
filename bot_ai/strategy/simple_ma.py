import ccxt
import logging
import json
import os
import time

def fetch_and_filter_pairs(cfg, use_cache=True, cache_ttl_hours=24):
    logger = logging.getLogger(__name__)
    cache_file = 'data/whitelist.json'

    # Проверяем кэш
    if use_cache and os.path.exists(cache_file):
        file_age_hours = (time.time() - os.path.getmtime(cache_file)) / 3600
        if file_age_hours < cache_ttl_hours:
            logger.info(f"Загружаем whitelist из {cache_file} (возраст {file_age_hours:.1f} ч.)")
            with open(cache_file, 'r', encoding='utf-8') as f:
                return json.load(f)
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

    logger.info
с


с@"
import ccxt
import logging
import pandas as pd

def run_strategy(cfg, pairs):
    logger = logging.getLogger(__name__)
    if not pairs:
        logger.warning("Список пар пуст — стратегия не запущена.")
        return

    exchange_class = getattr(ccxt, cfg.exchange)
    exchange = exchange_class({'enableRateLimit': True})

    logger.info(f"Запуск стратегии SMA для {len(pairs)} пар...")

    for symbol in pairs:
        try:
            # Загружаем последние 100 свечей по 5 минут
            ohlcv = exchange.fetch_ohlcv(symbol, timeframe='5m', limit=100)
            df = pd.DataFrame(ohlcv, columns=['time', 'open', 'high', 'low', 'close', 'volume'])

            # Считаем SMA
            df['SMA5'] = df['close'].rolling(window=5).mean()
            df['SMA20'] = df['close'].rolling(window=20).mean()

            last_row = df.iloc[-1]
            prev_row = df.iloc[-2]

            # Логика сигналов
            if prev_row['SMA5'] < prev_row['SMA20'] and last_row['SMA5'] > last_row['SMA20']:
                signal = "BUY"
            elif prev_row['SMA5'] > prev_row['SMA20'] and last_row['SMA5'] < last_row['SMA20']:
                signal = "SELL"
            else:
                signal = "HOLD"

            logger.info(f"{symbol}: {signal}")
        except Exception as e:
            logger.warning(f"Ошибка стратегии для {symbol}: {e}")
