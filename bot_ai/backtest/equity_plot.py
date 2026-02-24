# ============================================
# File: bot_ai/backtest/equity_plot.py
# Purpose: Plot equity curve from trade log CSV
# Format: UTF-8 without BOM
# ============================================

import os
import sys
import pandas as pd
import matplotlib.pyplot as plt

# === Ensure project root is in sys.path ===
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

def plot_equity_curve(csv_path):
    if not os.path.exists(csv_path):
        print(f"[ERROR] File not found: {csv_path}")
        return

    df = pd.read_csv(csv_path)
    if df.empty or "capital_after" not in df.columns:
        print(f"[ERROR] Invalid or empty trade log: {csv_path}")
        return

    symbol_timeframe = os.path.basename(csv_path).replace("_rsi_best_simulated.csv", "")
    output_path = f"backtest_logs/{symbol_timeframe}_equity.png"

    plt.figure(figsize=(10, 5))
    plt.plot(df["capital_after"], label="Equity Curve", color="blue", linewidth=2)
    plt.title(f"Equity Curve: {symbol_timeframe}")
    plt.xlabel("Trade #")
    plt.ylabel("Capital")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path)
    print(f"[EXPORT] Equity curve saved to {output_path}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=str, required=True, help="Path to trade log CSV")
    args = parser.parse_args()

    plot_equity_curve(args.file)
