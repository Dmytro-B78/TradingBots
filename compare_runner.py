# -*- coding: utf-8 -*-
# ============================================
# File: compare_runner.py
# Назначение: Запуск сравнения стратегий по конфигурации
# ============================================

import json
from bot_ai.backtest.strategy_comparator import compare_strategies

def load_config(path="config.json"):
    with open(path, "r", encoding="utf-8-sig") as f:
        return json.load(f)

if __name__ == "__main__":
    cfg = load_config()

    pairs = [s["pair"] for s in cfg.get("symbols", [])]
    strategies = cfg.get("compare", {}).get("strategies", ["breakout", "mean_reversion"])
    timeframe = cfg.get("backtest", {}).get("timeframe", "1h")
    capital = cfg.get("capital", 10000)
    risk_pct = cfg.get("risk_per_trade", 0.01) * 100

    compare_strategies(
        pairs=pairs,
        strategies=strategies,
        timeframe=timeframe,
        capital=capital,
        risk_pct=risk_pct
    )
