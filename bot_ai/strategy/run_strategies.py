# ============================================
# Path: C:\TradingBots\NT\bot_ai\strategy\run_strategies.py
# Purpose: Launch adaptive engine with pair filtering
# Supports multi-timeframe analysis and signal generation
# Format: UTF-8 without BOM, ready for production
# ============================================

import os
import json
import logging
import argparse
import pandas as pd
from bot_ai.config.config_loader import load_config
from bot_ai.strategy.adaptive_strategy_engine import analyze_and_select
from bot_ai.exchanges.exchange_loader import get_exchange_client
from bot_ai.utils.filter_pairs import filter_pairs

def load_whitelist(path="data/whitelist.json"):
    if not os.path.exists(path):
        logging.warning(f"⚠️ Whitelist file not found: {path}")
        return []
    with open(path, "r", encoding="utf-8-sig") as f:
        return json.load(f)

def fetch_ohlcv(client, symbol, timeframe, limit):
    try:
        return client.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
    except Exception as e:
        logging.error(f"❌ Failed to fetch OHLCV for {symbol} [{timeframe}]: {e}")
        return []

def export_signal(result, mode, timeframe):
    if mode != "paper" or not result:
        return

    output_dir = "paper_logs"
    os.makedirs(output_dir, exist_ok=True)

    df = pd.DataFrame([result["signal"]])
    filename = f"{output_dir}/{result['strategy']}_{result['symbol'].replace('/', '')}_{timeframe}_signal.csv"
    df.to_csv(filename, index=False)
    logging.info(f"[EXPORT] Signal saved to {filename}")

def run(cfg):
    whitelist = load_whitelist()
    if not whitelist:
        logging.info("📭 Whitelist is empty — no strategies will run.")
        return

    timeframes = cfg.get("timeframes", ["1h"])
    lookback = cfg.get("lookback_candles", 100)
    mode = cfg.get("mode", "paper")

    client = get_exchange_client(cfg)

    # === Filter pairs by volume, spread, volatility ===
    whitelist = filter_pairs(whitelist, client, cfg)
    if not whitelist:
        logging.info("🚫 No pairs passed filtering.")
        return

    for pair in whitelist:
        symbol = pair["symbol"]
        logging.info(f"📈 Processing pair: {symbol}")

        for tf in timeframes:
            ohlcv = fetch_ohlcv(client, symbol, tf, lookback)
            if not ohlcv:
                continue

            df = pd.DataFrame(ohlcv, columns=["time", "open", "high", "low", "close", "volume"])
            result = analyze_and_select(symbol, df, cfg)

            if result:
                logging.info(f"[SIGNAL] {result['symbol']} [{tf}] | {result['strategy']} → {result['signal']}")
                export_signal(result, mode, tf)

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

    logging.info(f"🚀 Starting strategy engine in {args.mode} mode")
    run(cfg)
