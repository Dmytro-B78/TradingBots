# ============================================
# File: bot_live_unified.py
# Purpose: Unified live strategy runner with debug logging
# Encoding: UTF-8
# ============================================

import logging
from bot_ai.utils.data import fetch_ohlcv
from bot_ai.strategy.strategy_loader import run_strategy
from bot_ai.strategy.strategy_catalog import STRATEGY_CATALOG

strategies = [
    "breakout",
    "mean_reversion",
    "rsi_macd",
    "ma_crossover",
    "range",
    "rsi_reversal",
    "sma_reversal",
    "volume_spike",
    "volatility_breakout",
    "zero_cross",
]

def main():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.StreamHandler()]
    )

    logging.info("Starting bot_live_unified.py")

    df = fetch_ohlcv("BTC/USDT", timeframe="1h", limit=500)
    if df is None or df.empty:
        logging.error("Failed to load OHLCV data. Exiting.")
        return

    for name in strategies:
        print(f"\n--- Running strategy: {name} ---")
        try:
            meta = STRATEGY_CATALOG.get(name, {})
            params = meta.get("default_params", {})
            logging.debug(f"Strategy: {name}")
            logging.debug(f"Parameters: {params}")
            logging.debug(f"DataFrame shape: {df.shape}")
            signal = run_strategy(name, df.copy(), params)
            print(f"Signal: {signal}")
        except Exception as e:
            logging.exception(f"Error running {name}")

if __name__ == "__main__":
    main()
