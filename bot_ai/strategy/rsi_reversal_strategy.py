# ============================================
# File: bot_ai/strategy/rsi_reversal_strategy.py
# Purpose: RSI reversal strategy with TP, trailing stop, holding period, and DB logging
# Format: UTF-8 without BOM
# ============================================

import pandas as pd
from bot_ai.core.signal import Signal
from bot_ai.core.strategy import Strategy
from bot_ai.indicators import calculate_rsi
from bot_ai.utils.logger import log_signal
from bot_ai.db import insert_trade


class RSIReversalStrategy(Strategy):
    """
    Classic RSI reversal strategy with:
    - oversold/overbought signals
    - trailing stop
    - take profit
    - max holding period
    - DB logging
    """

    def __init__(self, params):
        super().__init__(params, {})
        self.params = params
        self.symbol = params.get("symbol")
        self.rsi_period = params.get("rsi_period", 14)
        self.oversold = params.get("rsi_oversold", 30)
        self.overbought = params.get("rsi_overbought", 70)
        self.trailing_distance = params.get("trailing_stop_pct", 0.015)
        self.take_profit_pct = params.get("take_profit_pct", 0.02)
        self.max_holding_period = params.get("max_holding_period", 24)
        self.trades = []

    # ---------------------------------------------------------
    # Indicator calculation
    # ---------------------------------------------------------
    def calculate_indicators(self, df):
        df["rsi"] = calculate_rsi(df["close"], period=self.rsi_period)
        return df

    # ---------------------------------------------------------
    # Full-scan signal generation (for backtesting)
    # ---------------------------------------------------------
    def generate_signals(self, df):
        df["signal"] = None
        in_position = False
        entry_price = None
        entry_time = None
        trailing_stop_price = None

        for i in range(1, len(df)):
            rsi_prev = df["rsi"].iloc[i - 1]
            rsi_now = df["rsi"].iloc[i]
            price = df["close"].iloc[i]
            time = df["time"].iloc[i]

            log_signal(f"{time} | RSI: {rsi_now:.2f} | Price: {price:.4f}")

            if not in_position:
                if rsi_prev < self.oversold and rsi_now >= self.oversold:
                    df.at[df.index[i], "signal"] = "BUY"
                    entry_price = price
                    entry_time = time
                    trailing_stop_price = price * (1 - self.trailing_distance)
                    in_position = True
                    log_signal(f"Signal: BUY at {price:.4f}")

            else:
                holding_time = (time - entry_time).total_seconds() / 3600 if entry_time else 0

                if price >= entry_price * (1 + self.take_profit_pct):
                    df.at[df.index[i], "signal"] = "SELL"
                    in_position = False
                    log_signal(f"Take-Profit SELL at {price:.4f}")

                elif price <= trailing_stop_price:
                    df.at[df.index[i], "signal"] = "SELL"
                    in_position = False
                    log_signal(f"Trailing Stop SELL at {price:.4f}")

                elif holding_time >= self.max_holding_period:
                    df.at[df.index[i], "signal"] = "SELL"
                    in_position = False
                    log_signal(f"Max Holding SELL at {price:.4f}")

                elif price > entry_price:
                    new_trailing = price * (1 - self.trailing_distance)
                    if new_trailing > trailing_stop_price:
                        trailing_stop_price = new_trailing
                        log_signal(f"Trailing stop moved to {trailing_stop_price:.4f}")

                elif rsi_prev > self.overbought and rsi_now <= self.overbought:
                    df.at[df.index[i], "signal"] = "SELL"
                    in_position = False
                    log_signal(f"RSI SELL at {price:.4f}")

        return df

    # ---------------------------------------------------------
    # Single-step signal generation (for live trading)
    # ---------------------------------------------------------
    def generate_signal(self, df):
        df = self.calculate_indicators(df)
        if len(df) < 2:
            return None

        rsi_prev = df["rsi"].iloc[-2]
        rsi_now = df["rsi"].iloc[-1]
        price = df["close"].iloc[-1]
        time = df["time"].iloc[-1]

        log_signal(f"{time} | RSI: {rsi_now:.2f} | Price: {price:.4f}")

        if rsi_prev < self.oversold and rsi_now >= self.oversold:
            log_signal(f"Signal: BUY at {price:.4f}")
            return Signal(symbol=self.symbol, action="buy", price=price)

        if rsi_prev > self.overbought and rsi_now <= self.overbought:
            log_signal(f"Signal: SELL at {price:.4f}")
            return Signal(symbol=self.symbol, action="sell", price=price)

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
def rsi_reversal_strategy(params):
    """
    Factory function returning an instance of RSIReversalStrategy.
    Required by strategy_loader and test suite.
    """
    return RSIReversalStrategy(params)
