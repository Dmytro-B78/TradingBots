# ============================================
# File: bot_ai/strategy/mean_reversion.py
# Purpose: Mean reversion strategy with DB logging and backtest
# Format: UTF-8 without BOM
# ============================================

import pandas as pd
from bot_ai.core.signal import Signal
from bot_ai.core.strategy import Strategy
from bot_ai.utils.logger import log_signal
from bot_ai.db import insert_trade


class MeanReversionStrategy(Strategy):
    """
    Mean reversion strategy based on deviation from SMA.
    Includes:
    - deviation threshold entry
    - max holding period exit
    - DB logging
    """

    def __init__(self, params):
        super().__init__(params, {})
        self.params = params
        self.symbol = params.get("symbol")
        self.window = params.get("window", 20)
        self.threshold = params.get("threshold", 0.02)
        self.max_holding_period = params.get("max_holding_period", 24)
        self.trades = []

    # ---------------------------------------------------------
    # Indicator calculation
    # ---------------------------------------------------------
    def calculate_indicators(self, df):
        df["sma"] = df["close"].rolling(window=self.window).mean()
        df["deviation"] = (df["close"] - df["sma"]) / df["sma"]
        return df

    # ---------------------------------------------------------
    # Full-scan signal generation (for backtesting)
    # ---------------------------------------------------------
    def generate_signals(self, df):
        df["signal"] = None
        in_position = False
        entry_price = None
        entry_time = None

        for i in range(self.window, len(df)):
            row = df.iloc[i]
            price = row["close"]
            time = row["time"]
            deviation = row["deviation"]

            log_signal(f"{time} | Price: {price:.4f} | Deviation: {deviation:.4f}")

            if not in_position:
                if deviation < -self.threshold:
                    df.at[df.index[i], "signal"] = "BUY"
                    entry_price = price
                    entry_time = time
                    in_position = True
                    log_signal(f"Signal: BUY mean reversion at {price:.4f}")

                elif deviation > self.threshold:
                    df.at[df.index[i], "signal"] = "SELL"
                    entry_price = price
                    entry_time = time
                    in_position = True
                    log_signal(f"Signal: SELL mean reversion at {price:.4f}")

            else:
                holding_time = (time - entry_time).total_seconds() / 3600 if entry_time else 0

                if holding_time >= self.max_holding_period:
                    df.at[df.index[i], "signal"] = "SELL" if deviation < 0 else "BUY"
                    in_position = False
                    log_signal(f"Exit after max holding at {price:.4f}")

        return df

    # ---------------------------------------------------------
    # Single-step signal generation (for live trading)
    # ---------------------------------------------------------
    def generate_signal(self, df):
        df = self.calculate_indicators(df)
        if len(df) < self.window + 1:
            return None

        row = df.iloc[-1]
        price = row["close"]
        time = row["time"]
        deviation = row["deviation"]

        log_signal(f"{time} | Price: {price:.4f} | Deviation: {deviation:.4f}")

        if deviation < -self.threshold:
            log_signal(f"Signal: BUY mean reversion at {price:.4f}")
            return Signal(symbol=self.symbol, action="buy", price=price, time=time)

        if deviation > self.threshold:
            log_signal(f"Signal: SELL mean reversion at {price:.4f}")
            return Signal(symbol=self.symbol, action="sell", price=price, time=time)

        return None

    # ---------------------------------------------------------
    # Backtesting engine
    # ---------------------------------------------------------
    def backtest(self, df, initial_balance=1000, fee_rate=0.001):
        balance = initial_balance
        position = 0.0

        for i in range(len(df)):
            row = df.iloc[i]
            signal = row.get("signal")
            price = row["close"]

            if signal == "BUY" and balance > 0:
                qty = balance / price
                fee = qty * fee_rate
                position = qty - fee
                balance = 0
                equity = position * price

                trade = {
                    "symbol": self.symbol,
                    "signal": "BUY",
                    "price": price,
                    "time": row["time"],
                    "balance": balance,
                    "equity": equity
                }

                self.trades.append(trade)
                insert_trade(trade)

            elif signal == "SELL" and position > 0:
                proceeds = position * price
                fee = proceeds * fee_rate
                balance = proceeds - fee
                position = 0
                equity = balance

                trade = {
                    "symbol": self.symbol,
                    "signal": "SELL",
                    "price": price,
                    "time": row["time"],
                    "balance": balance,
                    "equity": equity
                }

                self.trades.append(trade)
                insert_trade(trade)

    # ---------------------------------------------------------
    # Backtest summary
    # ---------------------------------------------------------
    def summary(self, symbol):
        return pd.DataFrame(self.trades)


# ============================================================
# Factory function required by strategy_loader and tests
# ============================================================
def mean_reversion_strategy(params):
    """
    Factory function returning an instance of MeanReversionStrategy.
    Required by strategy_loader and test suite.
    """
    return MeanReversionStrategy(params)
