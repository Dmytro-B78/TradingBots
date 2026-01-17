# -*- coding: utf-8 -*-
# ============================================
# File: adaptive_strategy.py
# Назначение: Адаптивная стратегия с фильтрами ATR, ADX и тренда
# Поддержка мульти-таймфрейм фильтра (старший ТФ)
# ============================================

import pandas as pd
from bot_ai.filters.entry_filters import atr_filter, adx_filter
from bot_ai.indicators import calculate_atr, calculate_adx, calculate_sma
from bot_ai.data_loader import load_data

def higher_tf_trend_ok(higher_df: pd.DataFrame, lookback: int = 20) -> bool:
    """
    Проверка тренда на старшем таймфрейме: цена выше SMA → тренд вверх.
    """
    if len(higher_df) < lookback:
        return False
    sma = calculate_sma(higher_df["close"], period=lookback)
    return higher_df["close"].iloc[-1] > sma.iloc[-1]

def adaptive_strategy(pair: str, df: pd.DataFrame, config: dict) -> list:
    """
    Адаптивная стратегия с фильтрами ATR, ADX и тренда.
    """
    signals = []

    if len(df) < 50:
        return signals

    # === Фильтр ATR ===
    if not atr_filter(df, config):
        return signals

    # === Фильтр ADX ===
    if not adx_filter(df, config):
        return signals

    # === Мульти-таймфрейм фильтр ===
    if config.get("enable_mtf_filter", False):
        higher_tf = config.get("higher_tf", "4h")
        higher_df = load_data(pair, higher_tf, limit=100)
        if not higher_tf_trend_ok(higher_df):
            print(f"[FILTER:mtf] ❌ Тренд на {higher_tf} не подтверждён")
            return signals
        else:
            print(f"[FILTER:mtf] ✅ Тренд на {higher_tf} подтверждён")

    # === Пример генерации сигнала ===
    close = df["close"].iloc[-1]
    signal = {
        "pair": pair,
        "side": "BUY",
        "entry": close,
        "stop": close * (1 - config.get("stop_loss_pct", 0.02)),
        "target": close * (1 + config.get("stop_loss_pct", 0.02) * config.get("min_risk_reward_ratio", 1.5)),
        "strategy": "adaptive"
    }
    signals.append(signal)

    return signals
