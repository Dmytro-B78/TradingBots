import ccxt
import logging
import pandas as pd
import os
from datetime import datetime

def run_strategy(cfg, pairs):
    logger = logging.getLogger(__name__)
    if not pairs:
        logger.warning("Список пар пуст — стратегия не запущена.")
        return

    # Файл для записи сигналов
    os.makedirs('data', exist_ok=True)
    signals_file = 'data/signals.log'

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

            # Лог в консоль
            logger.info(f"{symbol}: {signal}")

            # Запись в файл
            with open(signals_file, 'a', encoding='utf-8') as f:
                f.write(f"{datetime.utcnow().isoformat()}Z,{symbol},{signal}\n")

        except Exception as e:
            logger.warning(f"Ошибка стратегии для {symbol}: {e}")