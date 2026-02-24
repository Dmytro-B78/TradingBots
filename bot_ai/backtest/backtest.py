# -*- coding: utf-8 -*-
# ============================================
# File: bot_ai/backtest/backtest.py
# Purpose: Backtest signals from CSV and generate summary report
# ============================================

import os
import pandas as pd
from datetime import datetime

# Constants
COMMISSION = 0.001
SLIPPAGE_PCT = 0.001
STOP_LOSS_PCT = 0.0075
TAKE_PROFIT_PCT = 0.005
MAX_HOLD_HOURS = 48

# Directories
INPUT_DIR = "paper_logs"
OUTPUT_DIR = "backtest_logs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Required columns in signal files
REQUIRED_COLUMNS = {"symbol", "entry_time", "signal", "price"}

def simulate_trade(entry_price, direction, future_candles):
    entry_price = entry_price * (1 + SLIPPAGE_PCT) if direction == "buy" else entry_price * (1 - SLIPPAGE_PCT)
    sl = entry_price * (1 - STOP_LOSS_PCT) if direction == "buy" else entry_price * (1 + STOP_LOSS_PCT)
    tp = entry_price * (1 + TAKE_PROFIT_PCT) if direction == "buy" else entry_price * (1 - TAKE_PROFIT_PCT)

    print(f"\n📈 New trade: {direction.upper()} @ {round(entry_price, 4)} → TP: {round(tp, 4)}, SL: {round(sl, 4)}")

    for i, row in future_candles.iterrows():
        high = row["high"]
        low = row["low"]
        close = row["close"]
        time = i.strftime("%Y-%m-%d %H:%M")

        print(f"  🕒 {time} | High: {high:.4f} | Low: {low:.4f}")

        if direction == "buy":
            if low <= sl:
                exit_price = sl * (1 - SLIPPAGE_PCT)
                print(f"  ❌ SL hit → Exit @ {round(exit_price, 4)}")
                return exit_price, -STOP_LOSS_PCT - 2 * COMMISSION
            if high >= tp:
                exit_price = tp * (1 - SLIPPAGE_PCT)
                print(f"  ✅ TP hit → Exit @ {round(exit_price, 4)}")
                return exit_price, TAKE_PROFIT_PCT - 2 * COMMISSION
        else:
            if high >= sl:
                exit_price = sl * (1 + SLIPPAGE_PCT)
                print(f"  ❌ SL hit → Exit @ {round(exit_price, 4)}")
                return exit_price, -STOP_LOSS_PCT - 2 * COMMISSION
            if low <= tp:
                exit_price = tp * (1 + SLIPPAGE_PCT)
                print(f"  ✅ TP hit → Exit @ {round(exit_price, 4)}")
                return exit_price, TAKE_PROFIT_PCT - 2 * COMMISSION

    exit_price = close * (1 - SLIPPAGE_PCT) if direction == "buy" else close * (1 + SLIPPAGE_PCT)
    pnl = (exit_price - entry_price) / entry_price if direction == "buy" else (entry_price - exit_price) / entry_price
    print(f"  ⏳ TTL exit → Exit @ {round(exit_price, 4)} | PnL: {round(pnl - 2 * COMMISSION, 4)}")
    return exit_price, pnl - 2 * COMMISSION

def backtest_file(file_path):
    df = pd.read_csv(file_path)
    if df.empty or not REQUIRED_COLUMNS.issubset(df.columns):
        print(f"⚠️ Skipped file (missing required columns): {file_path}")
        return []

    pair = df["symbol"].iloc[0]
    tf = "1h"
    candles_path = f"data/history/{pair.replace('/', '')}_{tf}.csv"
    if not os.path.exists(candles_path):
        print(f"⚠️ Missing historical data: {candles_path}")
        return []

    candles = pd.read_csv(candles_path)
    candles["time"] = pd.to_datetime(candles["time"])
    candles.set_index("time", inplace=True)

    results = []
    skipped = 0

    for _, signal in df.iterrows():
        entry_time = pd.to_datetime(signal["entry_time"], unit="ms")
        direction = signal["signal"]
        print(f"\n🔹 Signal: {direction.upper()} at {entry_time}")

        future = candles[candles.index >= entry_time].iloc[:MAX_HOLD_HOURS]
        in_index = entry_time in candles.index
        if future.empty or not in_index:
            print(f"  ⚠️ Skipped: entry_time in index = {in_index}, future empty = {future.empty}")
            skipped += 1
            continue

        entry_price = candles.at[entry_time, "open"]
        exit_price, pnl = simulate_trade(entry_price, direction, future)

        results.append({
            "symbol": pair,
            "entry_time": entry_time,
            "direction": direction,
            "entry_price": entry_price,
            "exit_price": exit_price,
            "pnl": round(pnl, 4)
        })

    if skipped > 0:
        print(f"\n⚠️ Skipped {skipped} signals due to missing candles at entry_time")

    return results

def run_backtest(config=None):
    print("Running backtest from paper_logs/")
    main()

def main():
    all_results = []
    for file in os.listdir(INPUT_DIR):
        if file.endswith(".csv"):
            path = os.path.join(INPUT_DIR, file)
            trades = backtest_file(path)
            if trades:
                df = pd.DataFrame(trades)
                out_path = os.path.join(OUTPUT_DIR, file.replace("_signals", "_bt"))
                df.to_csv(out_path, index=False)
                all_results.extend(trades)

    if all_results:
        df_all = pd.DataFrame(all_results)
        summary = df_all.groupby("symbol").agg(
            trades=("pnl", "count"),
            wins=("pnl", lambda x: (x > 0).sum()),
            losses=("pnl", lambda x: (x <= 0).sum()),
            avg_pnl=("pnl", "mean")
        ).reset_index()
        summary.to_csv(os.path.join(OUTPUT_DIR, "backtest_summary.csv"), index=False)
        print("✅ Backtest completed. Summary saved to backtest_logs/backtest_summary.csv")
    else:
        print("⚠️ No results found for backtest.")

if __name__ == "__main__":
    main()
