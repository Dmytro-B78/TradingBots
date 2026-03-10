# ============================================
# File: bot_ai/strategy/breakout.py
# Purpose: Breakout strategy with TP, SL, holding period, DB logging
# Format: UTF-8 without BOM
# ============================================

import pandas as pd
from bot_ai.core.signal import Signal
from bot_ai.core.strategy import Strategy
from bot_ai.utils.logger import log_signal
from bot_ai.db import insert_trade


class BreakoutStrategy(Strategy):
    """
    Breakout strategy based on high/low channel breakout.
    Includes:
    - breakout entry
    - take profit
    - stop loss
    - max holding period
    - DB logging
    """

    def __init__(self, params):
        super().__init__(params, {})
        self.params = params
        self.symbol = params.get("symbol")
        self.lookback = params.get("lookback", 20)
        self.take_profit_pct = params.get("take_profit_pct", 0.03)
        self.stop_loss_pct = params.get("stop_loss_pct", 0.01)
        self.max_holding_period = params.get("max_holding_period", 24)
        self.trades = []

    # ---------------------------------------------------------
    # Indicator calculation
    # ---------------------------------------------------------
    def calculate_indicators(self, df):
        df["high_max"] = df["high"].rolling(window=self.lookback).max()
        df["low_min"] = df["low"].rolling(window=self.lookback).min()
        return df

    # ---------------------------------------------------------
    # Full-scan signal generation (for backtesting)
    # ---------------------------------------------------------
    def generate_signals(self, df):
        df["signal"] = None
        in_position = False
        entry_price = None
        entry_time = None

        for i in range(self.lookback, len(df)):
            row = df.iloc[i]
            price = row["close"]
            time = row["time"]
            high_break = df["high_max"].iloc[i]
            low_break = df["low_min"].iloc[i]

            log_signal(f"{time} | Price: {price:.4f} | HighMax: {high_break:.4f} | LowMin: {low_break:.4f}")

            if not in_position:
                if price > high_break:
                    df.at[df.index[i], "signal"] = "BUY"
                    entry_price = price
                    entry_time = time
                    in_position = True
                    log_signal(f"Signal: BUY breakout at {price:.4f}")

            else:
                holding_time = (time - entry_time).total_seconds() / 3600 if entry_time else 0

                if price >= entry_price * (1 + self.take_profit_pct):
                    df.at[df.index[i], "signal"] = "SELL"
                    in_position = False
                    log_signal(f"Take-Profit SELL at {price:.4f}")

                elif price <= entry_price * (1 - self.stop_loss_pct):
                    df.at[df.index[i], "signal"] = "SELL"
                    in_position = False
                    log_signal(f"Stop-Loss SELL at {price:.4f}")

                elif holding_time >= self.max_holding_period:
                    df.at[df.index[i], "signal"] = "SELL"
                    in_position = False
                    log_signal(f"Max Holding SELL at {price:.4f}")

        return df

    # ---------------------------------------------------------
    # Single-step signal generation (for live trading)
    # ---------------------------------------------------------
    def generate_signal(self, df):
        df = self.calculate_indicators(df)
        if len(df) < self.lookback + 1:
            return None

        row = df.iloc[-1]
        price = row["close"]
        time = row["time"]
        high_break = row["high_max"]
        low_break = row["low_min"]

        log_signal(f"{time} | Price: {price:.4f} | HighMax: {high_break:.4f} | LowMin: {low_break:.4f}")

        if price > high_break:
            log_signal(f"Signal: BUY breakout at {price:.4f}")
            return Signal(symbol=self.symbol, action="buy", price=price, time=time)

        if price < low_break:
            log_signal(f"Signal: SELL breakdown at {price:.4f}")
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
def breakout_strategy(params):
    """
    Factory function returning an instance of BreakoutStrategy.
    Required by strategy_loader and test suite.
    """
    return BreakoutStrategy(params)
