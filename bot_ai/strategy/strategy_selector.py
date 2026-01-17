# -*- coding: utf-8 -*-
# ============================================
# 📂 File: bot_ai/strategy/strategy_selector.py
# 🧠 Назначение: Выбор и запуск стратегии
# ============================================

import json
import os
import pandas as pd

from .rsi_macd import RSIMACDStrategy
from .rsi_bbands import RSIBBandsStrategy
from .rsi_ichimoku import RSIIchimokuStrategy
from .volatile import VolatileStrategy
from .range import RangeStrategy

STRATEGY_MAP = {
    "rsi_macd": RSIMACDStrategy,
    "rsi_bbands": RSIBBandsStrategy,
    "rsi_ichimoku": RSIIchimokuStrategy,
    "volatile": VolatileStrategy,
    "range": RangeStrategy
}

def get_strategy(name: str, config: dict):
    strategy_cls = STRATEGY_MAP.get(name)
    if not strategy_cls:
        raise ValueError(f"❌ Неизвестная стратегия: {name}")
    return strategy_cls(config, config.get("pair", "BTCUSDT"), config.get("timeframe", "1h"))

def run_strategy(name: str, df: pd.DataFrame) -> dict:
    config_path = os.path.join("bot_ai", "config", f"{name}.json")
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"❌ Конфиг не найден: {config_path}")

    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    # 🔍 Отладка: выводим конфиг
    print(f"⚙️ Конфиг [{name}]: {config}")

    strategy = get_strategy(name, config)
    strategy.load_data(df)
    strategy.generate_signals()
    return strategy.run_backtest()
