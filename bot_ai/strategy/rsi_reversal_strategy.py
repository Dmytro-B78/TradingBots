# -*- coding: utf-8 -*-
# ============================================
# File: bot_ai/strategy/rsi_reversal_strategy.py
# Назначение: RSI стратегия разворота с параметрами из config.json
# ============================================

import pandas as pd

def rsi_reversal_strategy(pair: str, df: pd.DataFrame, config: dict) -> list:
    """
    RSI стратегия разворота тренда.
    Использует параметры из config["strategy_config"]["rsi_reversal"]
    """
    params = config.get("strategy_config", {}).get("rsi_reversal", {})
    rsi_period = params.get("rsi_period", 14)
    rsi_buy = params.get("rsi_buy_threshold", 30)
    rsi_sell = params.get("rsi_sell_threshold", 70)
    rr_ratio = params.get("risk_reward_ratio", 1.5)

    signals = []
    if df is None or df.empty or len(df) < rsi_period + 1:
        return signals

    delta = df["close"].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=rsi_period).mean()
    avg_loss = loss.rolling(window=rsi_period).mean()

    rs = avg_gain / avg_loss
    df["rsi"] = 100 - (100 / (1 + rs))

    rsi_prev = df["rsi"].iloc[-2]
    rsi_curr = df["rsi"].iloc[-1]
    price = df["close"].iloc[-1]

    if rsi_prev < rsi_buy and rsi_curr >= rsi_buy:
        target = round(price * (1 + 0.01 * rr_ratio), 2)
        stop = round(price * (1 - 0.01 * rr_ratio), 2)
        signals.append({
            "side": "BUY",
            "entry": price,
            "target": target,
            "stop": stop
        })

    elif rsi_prev > rsi_sell and rsi_curr <= rsi_sell:
        target = round(price * (1 - 0.01 * rr_ratio), 2)
        stop = round(price * (1 + 0.01 * rr_ratio), 2)
        signals.append({
            "side": "SELL",
            "entry": price,
            "target": target,
            "stop": stop
        })

    return signals
