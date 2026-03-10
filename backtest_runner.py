# ============================================
# File: C:\TradingBots\NT\backtest_runner.py
# Purpose: Run standalone backtest for a single strategy
# Format: UTF-8 without BOM
# ============================================

from bot_ai.strategy.rsi_reversal_strategy import RSIReversalStrategy
from bot_ai.metrics import calculate_metrics
import pandas as pd
import os

# Parameters
symbol = "BTCUSDT"
timeframe = "1h"
initial_balance = 1000
data_path = f"data/{symbol}_{timeframe}.csv"

# Load historical data
if not os.path.exists(data_path):
    raise FileNotFoundError(f"Missing data file: {data_path}")

df = pd.read_csv(data_path)
df["time"] = pd.to_datetime(df["time"])

# Strategy parameters
params = {
    "symbol": symbol,
    "rsi_period": 14,
    "rsi_oversold": 30,
    "rsi_overbought": 70,
    "trailing_stop_pct": 0.015,
    "take_profit_pct": 0.02,
    "max_holding_period": 24
}

# Run strategy
strategy = RSIReversalStrategy(params)
df = strategy.calculate_indicators(df)
df = strategy.generate_signals(df)
strategy.backtest(df, initial_balance=initial_balance)

# Output results
summary = strategy.summary(symbol)
if summary.empty:
    print("No trades executed.")
else:
    metrics = calculate_metrics(summary, initial_balance=initial_balance)
    print(f"Backtest results for {symbol} | {timeframe}")
    for k, v in metrics.items():
        print(f"{k:>20}: {v}")
