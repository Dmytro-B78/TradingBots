# ============================================
# File: C:\TradingBots\NT\bot_ai\strategy\base_strategy.py
# Purpose: Base strategy class with create_signal method (fixed: added import pandas)
# Encoding: UTF-8 without BOM
# ============================================

import logging
import pandas as pd
from bot_ai.core.signal import Signal

class BaseStrategy:
    def __init__(self, params: dict = None):
        self.params = params or {}

    def create_signal(self, action: str, df):
        """Construct a Signal object with the latest price and action."""
        price = df["close"].iloc[-1]
        time = df.index[-1]
        symbol = df["symbol"].iloc[-1] if "symbol" in df.columns else "UNKNOWN"

        if pd.isna(price):
            logging.warning(f"NaN price in signal: {action} {symbol} @ NaN [{time}]")
            price = None
        else:
            logging.debug(f"Creating signal: {action} {symbol} @ {price} [{time}]")

        return Signal(symbol=symbol, action=action, price=price, time=time)
