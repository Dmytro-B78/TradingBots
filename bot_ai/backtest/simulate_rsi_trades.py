# ============================================
# File: bot_ai/backtest/simulate_rsi_trades.py
# Purpose: Simulate RSI signals using Simulator class
# Format: UTF-8 without BOM
# ============================================

import argparse
import pandas as pd
from bot_ai.backtest.simulator import Simulator

def simulate_from_signals(file_path, initial_capital=1000, risk_per_trade=0.01):
    df = pd.read_csv(file_path)
    if df.empty or len(df) < 2:
        print("[INFO] Not enough signals to simulate.")
        return

    df = df.sort_values("time").reset_index(drop=True)
    pair = df["symbol"].iloc[0]
    timeframe = "1h"

    sim = Simulator(initial_capital, risk_per_trade, pair, timeframe)

    position = None
    for _, row in df.iterrows():
        side = row["action"].upper()
        time = row["time"]
        price = row["price"]

        if side == "BUY" and position is None:
            position = (time, side, price)
        elif side == "SELL" and position is not None:
            sim.execute_trade(position[0], "BUY", position[2])
            sim.execute_trade(time, "SELL", price)
            position = None

    report, trades_df = sim.get_report()

    print("\n=== Simulation Report ===")
    for k, v in report.items():
        print(f"{k.replace('_',' ').title():<20}: {v}")

    output_path = file_path.replace(".csv", "_simulated.csv")
    trades_df.to_csv(output_path, index=False)
    print(f"\n[EXPORT] Simulated trades saved to {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=str, required=True, help="Path to RSI signal CSV")
    parser.add_argument("--capital", type=float, default=1000)
    parser.add_argument("--risk", type=float, default=0.01)
    args = parser.parse_args()

    simulate_from_signals(args.file, args.capital, args.risk)
