# ============================================
# File: bot_ai/strategy/rsi_reversal_strategy.py
# Purpose: RSI-based reversal strategy with threshold cross detection
# Format: UTF-8 without BOM
# Compatible with: Signal, config, logging
# ============================================

import pandas as pd
import logging
from bot_ai.core.signal import Signal
from bot_ai.indicators import calculate_rsi

class RSIReversalStrategy:
    def __init__(self, config: dict):
        self.rsi_period = config.get("rsi_period", 14)
        self.oversold = config.get("rsi_oversold", 30)
        self.overbought = config.get("rsi_overbought", 70)

    def generate_signal(self, df: pd.DataFrame) -> Signal | None:
        if df is None or df.empty or len(df) < self.rsi_period + 2:
            logging.debug(f"[SKIP] RSI_Reversal | insufficient candles (len={len(df)})")
            return None

        df = df.copy()
        df["rsi"] = calculate_rsi(df["close"], self.rsi_period)

        prev = df.iloc[-2]
        curr = df.iloc[-1]
        symbol = curr.get("symbol", "UNKNOWN")

        logging.debug(f"[DEBUG] RSI_Reversal | rsi={curr['rsi']:.2f} prev_rsi={prev['rsi']:.2f}")

        # Buy signal: RSI crosses up from below oversold
        if prev["rsi"] < self.oversold and curr["rsi"] > self.oversold:
            signal = Signal("buy", symbol, df.index[-1],
                            entry_price=round(curr["close"], 8),
                            strategy_name="rsi_reversal")
            logging.info(f"[SIGNAL] {signal}")
            return signal

        # Sell signal: RSI crosses down from above overbought
        if prev["rsi"] > self.overbought and curr["rsi"] < self.overbought:
            signal = Signal("sell", symbol, df.index[-1],
                            entry_price=round(curr["close"], 8),
                            strategy_name="rsi_reversal")
            logging.info(f"[SIGNAL] {signal}")
            return signal

        logging.debug(f"[SKIP] RSI_Reversal | no threshold cross detected")
        return None
