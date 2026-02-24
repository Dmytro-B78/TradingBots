# ============================================
# File: bot_ai/backtest/simulate_top_rsi_configs.py
# Purpose: Simulate best RSI configuration with persistent position tracking
#          + auto-import fix for bot_ai root
# Format: UTF-8 without BOM
# ============================================

# -*- coding: utf-8 -*-
import sys
import os

# === Ensure project root is in sys.path ===
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import pandas as pd
from bot_ai.strategy.rsi_reversal_strategy import RSIReversalStrategy
from bot_ai.backtest.simulator import Simulator
from bot_ai.data_loader import load_data
from bot_ai.state.position_tracker import PositionTracker

def simulate_best_config(result_csv_path, initial_capital=1000, risk_per_trade=0.01, commission=0.001, stop_loss_pct=0.02):
    print("[DEBUG] Loading optimization results...")
    df_results = pd.read_csv(result_csv_path)
    if df_results.empty:
        print("[ERROR] Optimization results file is empty.")
        return

    if "score" not in df_results.columns:
        df_results["score"] = df_results["total_return"] - abs(df_results["max_drawdown"])

    best_row = df_results.sort_values("score", ascending=False).iloc[0]

    filename = os.path.basename(result_csv_path)
    symbol_timeframe = filename.replace("_rsi_grid_optimization.csv", "")
    parts = symbol_timeframe.split("_")
    if len(parts) < 2:
        print(f"[ERROR] Failed to parse symbol and timeframe from filename: {filename}")
        return

    symbol = parts[0]
    timeframe = parts[1]

    print(f"[DEBUG] Loading price data for {symbol} [{timeframe}]...")
    df = load_data(symbol, timeframe)
    if df is None or df.empty:
        print(f"[ERROR] Failed to load data for {symbol}")
        return

    print(f"\n=== Simulating Best Config ===")
    cfg = {
        "rsi_period": int(best_row["rsi_period"]),
        "rsi_oversold": int(best_row["oversold"]),
        "rsi_overbought": int(best_row["overbought"])
    }
    print(f"[DEBUG] Config: {cfg}")

    strategy = RSIReversalStrategy(cfg)
    signals = []

    for i in range(cfg["rsi_period"] + 1, len(df)):
        window = df.iloc[:i+1]
        signal = strategy.generate_signal(window)
        if signal:
            signals.append(signal)

    print(f"[DEBUG] Total signals: {len(signals)}")
    for s in signals:
        print(f"[DEBUG] Signal: {s.time} | {s.action} @ {s.price}")

    sim = Simulator(
        initial_capital=initial_capital,
        risk_per_trade=risk_per_trade,
        pair=symbol,
        timeframe=timeframe,
        commission=commission,
        stop_loss_pct=stop_loss_pct
    )

    tracker = PositionTracker(symbol, timeframe)
    saved = tracker.load()
    position = None

    if saved:
        print(f"[DEBUG] Loaded open position from file: {saved}")
        position = type("Signal", (), {
            "time": saved["open_time"],
            "price": saved["open_price"],
            "action": "BUY"
        })()

    for s in signals:
        if s.action.upper() == "BUY" and position is None:
            position = s
            tracker.save(s.time, s.price)
        elif s.action.upper() == "SELL" and position is not None:
            sim.execute_trade(position.time, "BUY", position.price)
            sim.execute_trade(s.time, "SELL", s.price)
            tracker.clear()
            position = None

    report, trades_df = sim.get_report()

    if position is not None:
        report["open_position_price"] = position.price
        report["open_position_time"] = position.time
        print(f"[DEBUG] Open position remains: {position.time} @ {position.price}")
    else:
        report["open_position_price"] = None
        report["open_position_time"] = None

    for k, v in cfg.items():
        report[k] = v

    print("\n--- Report ---")
    for k, v in report.items():
        print(f"{k.replace('_',' ').title():<22}: {v}")

    output_path = f"backtest_logs/{symbol}_{timeframe}_rsi_best_simulated.csv"
    trades_df.to_csv(output_path, index=False)
    print(f"[EXPORT] Trade log saved to {output_path}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=str, required=True, help="Path to RSI optimization CSV")
    args = parser.parse_args()

    simulate_best_config(args.file)
