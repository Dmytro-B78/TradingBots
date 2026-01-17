# -*- coding: utf-8 -*-
# ============================================
# File: bot_ai/strategy/ma_crossover_strategy.py
# Назначение: Стратегия пересечения скользящих средних (MA Crossover)
# ============================================

import pandas as pd

def ma_crossover_strategy(pair: str, df: pd.DataFrame, config: dict) -> list:
    """
    Стратегия: пересечение короткой и длинной скользящих средних.
    Использует параметры из config["strategy_config"]["ma_crossover"]
    """
    params = config.get("strategy_config", {}).get("ma_crossover", {})
    fast_period = params.get("fast_period", 10)
    slow_period = params.get("slow_period", 30)

    signals = []
    if df is None or df.empty or len(df) < slow_period + 1:
        return signals

    df["ma_fast"] = df["close"].rolling(window=fast_period).mean()
    df["ma_slow"] = df["close"].rolling(window=slow_period).mean()

    prev_fast = df["ma_fast"].iloc[-2]
    prev_slow = df["ma_slow"].iloc[-2]
    curr_fast = df["ma_fast"].iloc[-1]
    curr_slow = df["ma_slow"].iloc[-1]
    price = df["close"].iloc[-1]

    if prev_fast < prev_slow and curr_fast > curr_slow:
        signals.append({
            "side": "BUY",
            "entry": price,
            "target": round(price * 1.02, 2),
            "stop": round(price * 0.98, 2)
        })

    elif prev_fast > prev_slow and curr_fast < curr_slow:
        signals.append({
            "side": "SELL",
            "entry": price,
            "target": round(price * 0.98, 2),
            "stop": round(price * 1.02, 2)
        })

    return signals
