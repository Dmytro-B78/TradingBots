# ============================================
# File: bot_ai/strategy/ma_crossover_strategy.py
# Purpose: Moving Average Crossover strategy (SMA fast vs slow)
# Format: UTF-8 without BOM
# Compatible with: Signal, config, logging
# ============================================

import pandas as pd
import logging
from bot_ai.core.signal import Signal
from bot_ai.indicators import calculate_sma

class MACrossoverStrategy:
    def __init__(self, config: dict):
        self.fast_period = config.get("fast_period", 9)
        self.slow_period = config.get("slow_period", 21)

    def generate_signal(self, df: pd.DataFrame) -> Signal | None:
        if df is None or df.empty or len(df) < self.slow_period + 2:
            logging.debug(f"[SKIP] MA_Crossover | insufficient candles (len={len(df)})")
            return None

        df = df.copy()
        df["sma_fast"] = calculate_sma(df["close"], self.fast_period)
        df["sma_slow"] = calculate_sma(df["close"], self.slow_period)

        prev = df.iloc[-2]
        curr = df.iloc[-1]
        symbol = curr.get("symbol", "UNKNOWN")

        logging.debug(f"[DEBUG] MA_Crossover | fast={curr['sma_fast']:.8f} slow={curr['sma_slow']:.8f}")

        # Bullish crossover
        if prev["sma_fast"] < prev["sma_slow"] and curr["sma_fast"] > curr["sma_slow"]:
            signal = Signal("buy", symbol, df.index[-1],
                            entry_price=round(curr["close"], 8),
                            strategy_name="ma_crossover")
            logging.info(f"[SIGNAL] {signal}")
            return signal

        # Bearish crossover
        if prev["sma_fast"] > prev["sma_slow"] and curr["sma_fast"] < curr["sma_slow"]:
            signal = Signal("sell", symbol, df.index[-1],
                            entry_price=round(curr["close"], 8),
                            strategy_name="ma_crossover")
            logging.info(f"[SIGNAL] {signal}")
            return signal

        logging.debug(f"[SKIP] MA_Crossover | no crossover detected")
        return None
