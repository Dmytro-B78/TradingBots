# ============================================
# File: bot_ai/backtest/optimize_rsi_grid.py
# Purpose: Grid search optimization for RSI strategy parameters
#          + automatic simulation of best config
#          + full logging to .log file
#          + export best config to .json
# Format: UTF-8 without BOM
# ============================================

import itertools
import pandas as pd
import subprocess
import os
import sys
import json
import logging
from datetime import datetime
from bot_ai.strategy.rsi_reversal_strategy import RSIReversalStrategy
from bot_ai.backtest.simulator import Simulator
from bot_ai.data_loader import load_data

# === Setup logging ===
def setup_logger(symbol, timeframe):
    log_dir = "backtest_logs"
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, f"{symbol}_{timeframe}_optimize.log")

    logging.basicConfig(
        filename=log_path,
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(message)s",
        encoding="utf-8"
    )
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(logging.INFO)
    formatter = logging.Formatter("[%(levelname)s] %(message)s")
    console.setFormatter(formatter)
    logging.getLogger().addHandler(console)

    logging.info(f"Logging started: {log_path}")
    return log_path

# === Grid search runner ===
def run_grid_search(symbol, timeframe, initial_capital=1000, risk_per_trade=0.01, commission=0.001, stop_loss_pct=0.02):
    log_path = setup_logger(symbol, timeframe)

    rsi_periods = range(6, 23, 2)
    oversold_levels = range(15, 41, 5)
    overbought_levels = range(60, 91, 5)

    results = []

    df = load_data(symbol, timeframe)
    if df is None or df.empty:
        logging.error(f"Failed to load data for {symbol}")
        return

    total_combinations = sum(1 for _ in itertools.product(rsi_periods, oversold_levels, overbought_levels))
    tested = 0

    for rsi_period, oversold, overbought in itertools.product(rsi_periods, oversold_levels, overbought_levels):
        tested += 1
        if oversold >= overbought:
            continue

        cfg = {
            "rsi_period": rsi_period,
            "rsi_oversold": oversold,
            "rsi_overbought": overbought
        }

        logging.info(f"[{tested}/{total_combinations}] Testing: {cfg}")

        strategy = RSIReversalStrategy(cfg)
        signals = []

        for i in range(rsi_period + 1, len(df)):
            window = df.iloc[:i+1]
            signal = strategy.generate_signal(window)
            if signal:
                signals.append(signal)

        if len(signals) < 2:
            continue

        sim = Simulator(
            initial_capital=initial_capital,
            risk_per_trade=risk_per_trade,
            pair=symbol,
            timeframe=timeframe,
            commission=commission,
            stop_loss_pct=stop_loss_pct
        )

        position = None
        for s in signals:
            if s.action.upper() == "BUY" and position is None:
                position = s
            elif s.action.upper() == "SELL" and position is not None:
                sim.execute_trade(position.time, "BUY", position.price)
                sim.execute_trade(s.time, "SELL", s.price)
                position = None

        report, _ = sim.get_report()
        score = report["total_return"] - abs(report["max_drawdown"])
        report.update({
            "rsi_period": rsi_period,
            "oversold": oversold,
            "overbought": overbought,
            "score": round(score, 4)
        })
        results.append(report)

    if not results:
        logging.warning("No valid parameter combinations produced trades.")
        return

    df_results = pd.DataFrame(results)
    df_results = df_results.sort_values("score", ascending=False)
    output_csv = f"backtest_logs/{symbol.replace('/', '')}_{timeframe}_rsi_grid_optimization.csv"
    df_results.to_csv(output_csv, index=False)
    logging.info(f"Grid search results saved to {output_csv}")

    # === Export best config to JSON ===
    best = df_results.iloc[0].to_dict()
    best_config = {
        "symbol": symbol,
        "timeframe": timeframe,
        "rsi_period": int(best["rsi_period"]),
        "oversold": int(best["oversold"]),
        "overbought": int(best["overbought"]),
        "score": best["score"],
        "total_return": best["total_return"],
        "max_drawdown": best["max_drawdown"],
        "winrate": best["winrate"],
        "sharpe_ratio": best["sharpe_ratio"]
    }
    output_json = f"backtest_logs/{symbol}_{timeframe}_best_config.json"
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(best_config, f, indent=2)
    logging.info(f"Best config exported to {output_json}")

    # === Auto-run simulation of best config ===
    logging.info("Launching simulation of best config...")
    subprocess.run([
        "python",
        "bot_ai/backtest/simulate_top_rsi_configs.py",
        "--file", output_csv
    ])

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--symbol", type=str, required=True)
    parser.add_argument("--timeframe", type=str, default="1h")
    args = parser.parse_args()

    run_grid_search(args.symbol, args.timeframe)
