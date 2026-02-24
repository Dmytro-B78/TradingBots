# ============================================
# File: bot_ai/strategy/volatility_breakout_strategy.py
# Purpose: Volatility breakout strategy using ATR-based range expansion
# Format: UTF-8 without BOM
# Compatible with: Signal, config, logging
# ============================================

import pandas as pd
import logging
from bot_ai.core.signal import Signal
from bot_ai.indicators import calculate_atr

class VolatilityBreakoutStrategy:
    def __init__(self, config: dict):
        self.atr_period = config.get("atr_period", 14)
        self.atr_multiplier = config.get("atr_multiplier", 1.5)

    def generate_signal(self, df: pd.DataFrame) -> Signal | None:
        if df is None or df.empty or len(df) < self.atr_period + 2:
            logging.debug(f"[SKIP] VolatilityBreakout | insufficient candles (len={len(df)})")
            return None

        df = df.copy()
        df["atr"] = calculate_atr(df, self.atr_period)

        prev = df.iloc[-2]
        curr = df.iloc[-1]
        symbol = curr.get("symbol", "UNKNOWN")

        breakout_range = prev["high"] - prev["low"]
        atr = prev["atr"]
        threshold = atr * self.atr_multiplier

        logging.debug(f"[DEBUG] VolatilityBreakout | range={breakout_range:.8f} atr={atr:.8f} threshold={threshold:.8f}")

        if breakout_range > threshold:
            if curr["close"] > prev["high"]:
                signal = Signal("buy", symbol, df.index[-1],
                                entry_price=round(curr["close"], 8),
                                strategy_name="volatility_breakout")
                logging.info(f"[SIGNAL] {signal}")
                return signal
            elif curr["close"] < prev["low"]:
                signal = Signal("sell", symbol, df.index[-1],
                                entry_price=round(curr["close"], 8),
                                strategy_name="volatility_breakout")
                logging.info(f"[SIGNAL] {signal}")
                return signal

        logging.debug(f"[SKIP] VolatilityBreakout | no breakout detected")
        return None
