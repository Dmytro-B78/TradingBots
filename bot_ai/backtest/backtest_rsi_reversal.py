# ============================================
# File: bot_ai/backtest/backtest_rsi_reversal.py
# Purpose: Backtest RSIReversalStrategy using ccxt client
# Format: UTF-8 without BOM
# Compatible with: RSIReversalStrategy, Signal, config.json
# ============================================

import os
import logging
import argparse
import pandas as pd
import ccxt
from bot_ai.strategy.rsi_reversal_strategy import RSIReversalStrategy
from bot_ai.core.signal import Signal
from bot_ai.config.config_loader import load_config

def load_data(client, symbol, timeframe, limit):
    try:
        ohlcv = client.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
        df = pd.DataFrame(ohlcv, columns=["time", "open", "high", "low", "close", "volume"])
        df["symbol"] = symbol
        df.set_index("time", inplace=True)
        return df
    except Exception as e:
        logging.error(f"Failed to load data for {symbol}: {e}")
        return pd.DataFrame()

def backtest_rsi_reversal(cfg, symbol, timeframe):
    client = ccxt.binance()
    lookback = cfg.get("backtest", {}).get("lookback_bars", 200)

    df = load_data(client, symbol, timeframe, lookback)
    if df.empty:
        return

    strategy = RSIReversalStrategy(cfg)
    signals = []

    for i in range(cfg["rsi_period"] + 1, len(df)):
        window = df.iloc[:i+1]
        signal = strategy.generate_signal(window)
        if signal:
            signals.append(signal.to_dict())

    if not signals:
        logging.info(f"No signals generated for {symbol} [{timeframe}]")
        return

    output_dir = "backtest_logs"
    os.makedirs(output_dir, exist_ok=True)
    filename = f"{output_dir}/{symbol.replace('/', '')}_{timeframe}_rsi_reversal_backtest.csv"
    pd.DataFrame(signals).to_csv(filename, index=False)
    logging.info(f"Backtest results saved to {filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, required=True)
    parser.add_argument("--symbol", type=str, required=True)
    parser.add_argument("--timeframe", type=str, default="1h")
    parser.add_argument("--log-level", type=str, default="INFO")
    args = parser.parse_args()

    logging.basicConfig(
        level=getattr(logging, args.log_level.upper(), logging.INFO),
        format="%(asctime)s [%(levelname)s] %(message)s"
    )

    cfg = load_config(args.config)
    logging.info(f"Running RSIReversalStrategy backtest on {args.symbol} [{args.timeframe}]")
    backtest_rsi_reversal(cfg, args.symbol, args.timeframe)
