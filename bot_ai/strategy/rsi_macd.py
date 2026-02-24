# ============================================
# File: C:\TradingBots\NT\bot_ai\strategy\rsi_macd.py
# Purpose: RSI + MACD strategy class with debug logging
# Encoding: UTF-8 without BOM
# ============================================

import pandas as pd
import logging
from bot_ai.strategy.base_strategy import BaseStrategy
from bot_ai.core.signal import Signal

class RsiMacdStrategy(BaseStrategy):
    def generate_signal(self, df: pd.DataFrame, params: dict):
        rsi_period = params.get("rsi_period", 14)
        macd_fast = params.get("macd_fast", 12)
        macd_slow = params.get("macd_slow", 26)
        macd_signal = params.get("macd_signal", 9)
        rsi_lower = params.get("rsi_lower", 30)
        rsi_upper = params.get("rsi_upper", 70)

        # Calculate RSI
        delta = df["close"].diff()
        gain = delta.where(delta > 0, 0.0)
        loss = -delta.where(delta < 0, 0.0)
        avg_gain = gain.rolling(window=rsi_period).mean()
        avg_loss = loss.rolling(window=rsi_period).mean()
        rs = avg_gain / avg_loss
        df["rsi"] = 100 - (100 / (1 + rs))

        # Calculate MACD
        df["ema_fast"] = df["close"].ewm(span=macd_fast, adjust=False).mean()
        df["ema_slow"] = df["close"].ewm(span=macd_slow, adjust=False).mean()
        df["macd"] = df["ema_fast"] - df["ema_slow"]
        df["macd_signal"] = df["macd"].ewm(span=macd_signal, adjust=False).mean()

        logging.debug("RSI_MACD | Last 5 rows:\n" + df[["close", "rsi", "macd", "macd_signal"]].tail().to_string())

        rsi = df["rsi"].iloc[-1]
        macd = df["macd"].iloc[-1]
        macd_sig = df["macd_signal"].iloc[-1]
        price = df["close"].iloc[-1]
        timestamp = df.index[-1]

        if rsi < rsi_lower and macd > macd_sig:
            return Signal(action="buy", price=price, timestamp=timestamp)
        elif rsi > rsi_upper and macd < macd_sig:
            return Signal(action="sell", price=price, timestamp=timestamp)

        logging.debug(f"RSI_MACD | No signal: rsi={rsi:.2f}, macd={macd:.2f}, signal={macd_sig:.2f}, price={price}")
        return None
