# bot_ai/backtest/backtest_runner.py
# Entry point for CLI backtest execution with logging

import os
import csv
from bot_ai.backtest.backtest_engine import run_backtest

def main(pair, timeframe, strategy="rsi", rsi_threshold=50, capital=10000, risk_pct=0.01):
    report = run_backtest(
        pair=pair,
        timeframe=timeframe,
        strategy=strategy,
        rsi_threshold=rsi_threshold,
        capital=capital,
        risk_pct=risk_pct
    )

    if report is None:
        print(f"⚠️ Skipped: no signals for {pair} [{timeframe}]")
        return

    print("Backtest Report")
    print("-------------------------")
    for key, value in report.items():
        if isinstance(value, float):
            if "capital" in key.lower():
                print(f"{key.replace('_', ' ').title()}: ${value:,.2f}")
            else:
                print(f"{key.replace('_', ' ').title()}: {value}")
        else:
            print(f"{key.replace('_', ' ').title()}: {value}")

    os.makedirs("logs", exist_ok=True)
    results_path = "logs/results.csv"
    file_exists = os.path.exists(results_path)
    with open(results_path, mode="a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["symbol", "timeframe", "final_balance", "total_trades", "win_rate", "drawdown"])
        writer.writerow([
            pair,
            timeframe,
            round(report.get("final_balance", 2), 2),
            report.get("total_trades", 0),
            round(report.get("win_rate", 4), 4),
            round(report.get("max_drawdown", 4), 4)
        ])
