# -*- coding: utf-8 -*-
# ============================================
# File: live_trader.py
# Purpose: Entry point for paper/live trading
# Format: UTF-8 without BOM
# Restored to run_trading_loop for full trading loop
# ============================================

import argparse
import json
import os
from bot_ai.paper_trader import run_trading_loop

def load_config(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, default="config.json")
    parser.add_argument("--mode", type=str, choices=["paper", "live"], default="paper")
    parser.add_argument("--symbol", type=str, required=True)
    parser.add_argument("--strategy", type=str, required=True)
    parser.add_argument("--adaptive", action="store_true")
    parser.add_argument("--balance", type=float, default=1000)
    args = parser.parse_args()

    cfg = load_config(args.config)
    cfg["mode"] = args.mode
    cfg["symbol"] = args.symbol
    cfg["strategy"] = args.strategy
    cfg["adaptive"] = args.adaptive
    cfg["balance"] = args.balance

    print(f"🚀 Запуск {args.mode}-трейдинга | {args.symbol} | Стратегия: {args.strategy}")

    run_trading_loop(cfg)

if __name__ == "__main__":
    main()
