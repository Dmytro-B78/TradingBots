# ============================================
# File: C:\TradingBots\NT\run_live.py
# Purpose: Live/paper trading runner with DB integration
# Format: UTF-8 without BOM
# ============================================

import time
import pandas as pd
from bot_ai.strategy.rsi_reversal_strategy import RSIReversalStrategy
from bot_ai.core.signal import Signal
from bot_ai.utils.logger import log_signal
from bot_ai.db import init_db, insert_trade

def fetch_latest_data(symbol, interval="1h", limit=100):
    # Replace with actual data fetch logic
    now = pd.Timestamp.utcnow()
    times = pd.date_range(end=now, periods=limit, freq=interval.upper())
    prices = pd.Series([100 + i * 0.1 for i in range(limit)])
    df = pd.DataFrame({"time": times, "close": prices})
    return df

def execute_trade(signal: Signal, balance: float, position: float, fee_rate=0.001):
    price = signal.price
    time = signal.time
    if signal.action == "buy" and balance > 0:
        qty = balance / price
        fee = qty * fee_rate
        position = qty - fee
        balance = 0
        equity = position * price
    elif signal.action == "sell" and position > 0:
        proceeds = position * price
        fee = proceeds * fee_rate
        balance = proceeds - fee
        position = 0
        equity = balance
    else:
        return balance, position

    trade = {
        "symbol": signal.symbol,
        "signal": signal.action.upper(),
        "price": price,
        "time": time,
        "balance": balance,
        "equity": equity
    }
    insert_trade(trade)
    log_signal(str(signal))
    return balance, position

def run_live():
    init_db()
    params = {
        "symbol": "BTCUSDT",
        "rsi_period": 14,
        "rsi_oversold": 30,
        "rsi_overbought": 70,
        "trailing_stop_pct": 0.015,
        "take_profit_pct": 0.02,
        "max_holding_period": 24
    }

    strategy = RSIReversalStrategy(params)
    balance = 1000
    position = 0.0

    while True:
        df = fetch_latest_data(params["symbol"])
        signal = strategy.generate_signal(df)
        if signal:
            balance, position = execute_trade(signal, balance, position)
        time.sleep(60)

if __name__ == "__main__":
    run_live()
