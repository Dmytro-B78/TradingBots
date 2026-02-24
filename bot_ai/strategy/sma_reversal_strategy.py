# ============================================
# File: bot_ai/strategy/sma_reversal_strategy.py
# Purpose: SMA-based reversal strategy using price cross of moving average
# Format: UTF-8 without BOM
# Compatible with: Signal, config, logging
# ============================================

import pandas as pd
import logging
from bot_ai.core.signal import Signal
from bot_ai.indicators import calculate_sma

class SMAReversalStrategy:
    def __init__(self, config: dict):
        self.sma_period = config.get("sma_period", 20)

    def generate_signal(self, df: pd.DataFrame) -> Signal | None:
        if df is None or df.empty or len(df) < self.sma_period + 2:
            logging.debug(f"[SKIP] SMA_Reversal | insufficient candles (len={len(df)})")
            return None

        df = df.copy()
        df["sma"] = calculate_sma(df["close"], self.sma_period)

        prev = df.iloc[-2]
        curr = df.iloc[-1]
        symbol = curr.get("symbol", "UNKNOWN")

        logging.debug(f"[DEBUG] SMA_Reversal | close={curr['close']:.8f} sma={curr['sma']:.8f} prev_close={prev['close']:.8f} prev_sma={prev['sma']:.8f}")

        # Buy signal: price crosses above SMA
        if prev["close"] < prev["sma"] and curr["close"] > curr["sma"]:
            signal = Signal("buy", symbol, df.index[-1],
                            entry_price=round(curr["close"], 8),
                            strategy_name="sma_reversal")
            logging.info(f"[SIGNAL] {signal}")
            return signal

        # Sell signal: price crosses below SMA
        if prev["close"] > prev["sma"] and curr["close"] < curr["sma"]:
            signal = Signal("sell", symbol, df.index[-1],
                            entry_price=round(curr["close"], 8),
                            strategy_name="sma_reversal")
            logging.info(f"[SIGNAL] {signal}")
            return signal

        logging.debug(f"[SKIP] SMA_Reversal | no SMA cross detected")
        return None
