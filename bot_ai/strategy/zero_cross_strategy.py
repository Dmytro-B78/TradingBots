# ============================================
# File: bot_ai/strategy/zero_cross_strategy.py
# Purpose: Strategy based on zero-line cross of MACD histogram
# Format: UTF-8 without BOM
# Compatible with: Signal, config, logging
# ============================================

import pandas as pd
import logging
from bot_ai.core.signal import Signal
from bot_ai.indicators import calculate_macd

class ZeroCrossStrategy:
    def __init__(self, config: dict):
        self.macd_fast = config.get("macd_fast", 12)
        self.macd_slow = config.get("macd_slow", 26)
        self.macd_signal = config.get("macd_signal", 9)

    def generate_signal(self, df: pd.DataFrame) -> Signal | None:
        if df is None or df.empty or len(df) < self.macd_slow + 2:
            logging.debug(f"[SKIP] ZeroCross | insufficient candles (len={len(df)})")
            return None

        df = df.copy()
        macd_line, signal_line, hist = calculate_macd(df["close"], self.macd_fast, self.macd_slow, self.macd_signal)
        df["macd_hist"] = hist

        prev = df.iloc[-2]
        curr = df.iloc[-1]
        symbol = curr.get("symbol", "UNKNOWN")

        logging.debug(f"[DEBUG] ZeroCross | prev_hist={prev['macd_hist']:.6f} curr_hist={curr['macd_hist']:.6f}")

        # Buy signal: histogram crosses above zero
        if prev["macd_hist"] < 0 and curr["macd_hist"] > 0:
            signal = Signal("buy", symbol, df.index[-1],
                            entry_price=round(curr["close"], 8),
                            strategy_name="zero_cross")
            logging.info(f"[SIGNAL] {signal}")
            return signal

        # Sell signal: histogram crosses below zero
        if prev["macd_hist"] > 0 and curr["macd_hist"] < 0:
            signal = Signal("sell", symbol, df.index[-1],
                            entry_price=round(curr["close"], 8),
                            strategy_name="zero_cross")
            logging.info(f"[SIGNAL] {signal}")
            return signal

        logging.debug(f"[SKIP] ZeroCross | no zero-line cross detected")
        return None
