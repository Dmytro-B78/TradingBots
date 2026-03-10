# ============================================
# File: bot_ai/backtest/analyze_backtest_results.py
# Purpose: Analyze RSIReversalStrategy backtest signals and compute metrics
# Format: UTF-8 without BOM
# ============================================

import argparse
import pandas as pd
import os

def analyze_signals(path):
    if not os.path.exists(path):
        print(f"[ERROR] File not found: {path}")
        return

    df = pd.read_csv(path)
    if df.empty or len(df) < 2:
        print("[INFO] Not enough signals to analyze.")
        return

    df = df.sort_values("time").reset_index(drop=True)

    trades = []
    position = None

    for _, row in df.iterrows():
        if row["action"] == "buy" and position is None:
            position = row
        elif row["action"] == "sell" and position is not None:
            entry = position["price"]
            exit = row["price"]
            pnl = (exit - entry) / entry
            trades.append({
                "entry_time": position["time"],
                "exit_time": row["time"],
                "entry_price": entry,
                "exit_price": exit,
                "pnl_pct": pnl * 100
            })
            position = None

    if not trades:
        print("[INFO] No completed trades found.")
        return

    trades_df = pd.DataFrame(trades)
    total_return = trades_df["pnl_pct"].sum()
    win_rate = (trades_df["pnl_pct"] > 0).mean() * 100
    avg_win = trades_df[trades_df["pnl_pct"] > 0]["pnl_pct"].mean()
    avg_loss = trades_df[trades_df["pnl_pct"] < 0]["pnl_pct"].mean()
    max_drawdown = trades_df["pnl_pct"].cumsum().min()

    print("\n=== Backtest Metrics ===")
    print(f"Total Trades     : {len(trades_df)}")
    print(f"Total Return     : {total_return:.2f}%")
    print(f"Win Rate         : {win_rate:.2f}%")
    print(f"Avg Win          : {avg_win:.2f}%")
    print(f"Avg Loss         : {avg_loss:.2f}%")
    print(f"Max Drawdown     : {max_drawdown:.2f}%")

    trades_df.to_csv(path.replace(".csv", "_trades.csv"), index=False)
    print(f"\n[EXPORT] Trade log saved to {path.replace('.csv', '_trades.csv')}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=str, required=True, help="Path to backtest signal CSV")
    args = parser.parse_args()
    analyze_signals(args.file)
