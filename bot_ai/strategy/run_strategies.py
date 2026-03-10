# ============================================
# File: bot_ai/strategy/run_strategies.py
# Purpose: Run RSIReversalStrategy only (temporary override)
# Format: UTF-8 without BOM
# Compatible with: config.json, whitelist.json, Signal, logging
# ============================================

import os
import json
import logging
import argparse
import pandas as pd
from bot_ai.config.config_loader import load_config
from bot_ai.strategy.rsi_reversal_strategy import RSIReversalStrategy
from bot_ai.exchanges.exchange_loader import get_exchange_client
from bot_ai.utils.filter_pairs import filter_pairs

def load_whitelist(path="data/whitelist.json"):
    if not os.path.exists(path):
        logging.warning(f"Whitelist file not found: {path}")
        return []
    with open(path, "r", encoding="utf-8-sig") as f:
        return json.load(f)

def fetch_ohlcv(client, symbol, timeframe, limit):
    try:
        return client.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
    except Exception as e:
        logging.error(f"Failed to fetch OHLCV for {symbol} [{timeframe}]: {e}")
        return []

def export_signal(signal, mode, timeframe):
    if mode != "paper" or not signal:
        return

    output_dir = "paper_logs"
    os.makedirs(output_dir, exist_ok=True)

    df = pd.DataFrame([signal.to_dict()])
    filename = f"{output_dir}/{signal.symbol.replace('/', '')}_{timeframe}_rsi_reversal_signal.csv"
    df.to_csv(filename, index=False)
    logging.info(f"Signal saved to {filename}")

def run(cfg):
    whitelist = load_whitelist()
    if not whitelist:
        logging.info("Whitelist is empty — skipping execution")
        return

    timeframes = cfg.get("timeframes", ["1h"])
    lookback = cfg.get("lookback_candles", 100)
    mode = cfg.get("mode", "paper")

    client = get_exchange_client(cfg)
    whitelist = filter_pairs(whitelist, client, cfg)
    if not whitelist:
        logging.info("No pairs passed filtering")
        return

    strategy = RSIReversalStrategy(cfg)

    for pair in whitelist:
        symbol = pair["symbol"]
        logging.info(f"Processing pair: {symbol}")

        for tf in timeframes:
            ohlcv = fetch_ohlcv(client, symbol, tf, lookback)
            if not ohlcv:
                continue

            df = pd.DataFrame(ohlcv, columns=["time", "open", "high", "low", "close", "volume"])
            df["symbol"] = symbol
            df.set_index("time", inplace=True)

            signal = strategy.generate_signal(df)
            if signal:
                logging.info(f"Signal: {signal}")
                export_signal(signal, mode, tf)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, required=True)
    parser.add_argument("--mode", type=str, default="paper")
    parser.add_argument("--log-level", type=str, default="INFO")
    args = parser.parse_args()

    logging.basicConfig(
        level=getattr(logging, args.log_level.upper(), logging.INFO),
        format="%(asctime)s [%(levelname)s] %(message)s"
    )

    cfg = load_config(args.config)
    cfg["mode"] = args.mode

    logging.info(f"Running RSIReversalStrategy in {args.mode} mode")
    run(cfg)
