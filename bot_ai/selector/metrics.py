# ============================================
# File: bot_ai/selector/metrics.py
# Purpose: Calculate volatility using Binance SDK (no CCXT)
# Encoding: UTF-8
# ============================================

import logging
import statistics

def calculate_volatility(client, symbol, interval="5m", limit=100):
    try:
        klines = client.klines(symbol=symbol, interval=interval, limit=limit)
        closes = [float(k[4]) for k in klines if float(k[4]) > 0]

        if len(closes) < 2:
            logging.warning(f"[VOLATILITY] Not enough data for {symbol}")
            return None

        returns = [(closes[i] - closes[i - 1]) / closes[i - 1] for i in range(1, len(closes))]
        volatility = statistics.stdev(returns)
        return volatility

    except Exception as e:
        logging.error(f"[VOLATILITY] Failed to calculate for {symbol}: {e}")
        return None
