# -*- coding: utf-8 -*-
# ============================================
# File: pipeline_full.py
# Назначение: Расширенный отбор пар с выбором стратегии
# ============================================

from selector.filters import volume_ok, trend_ok, riskguard_ok
from selector.trend_utils import is_trending
from bot_ai.data_loader import load_data

DEFAULT_INTERVAL = "1h"
DEFAULT_QTY = 0.01

def choose_strategy(df, config) -> str:
    """
    Простая логика выбора стратегии:
    - если тренд есть → ma_crossover
    - иначе → rsi_reversal
    """
    if trend_ok(df, config):
        return "ma_crossover"
    return "rsi_reversal"

def get_active_symbols(pairs: list, config: dict) -> list:
    """
    Возвращает список пар с рекомендованной стратегией и параметрами.
    """
    active = []

    for pair in pairs:
        df = load_data(pair, DEFAULT_INTERVAL, limit=100)
        if df is None or len(df) < 50:
            continue

        # === Фильтры ===
        if not volume_ok(df, config):
            print(f"[FILTER:volume] ❌ {pair}")
            continue
        if not riskguard_ok(pair, config):
            print(f"[FILTER:risk] ❌ {pair}")
            continue

        # === Выбор стратегии ===
        strategy = choose_strategy(df, config)
        print(f"[SELECTOR] ✅ {pair} → {strategy}")

        active.append({
            "pair": pair,
            "strategy": strategy,
            "interval": DEFAULT_INTERVAL,
            "qty": DEFAULT_QTY
        })

    return active
