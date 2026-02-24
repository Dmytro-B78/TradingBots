# ============================================
# File: C:\TradingBots\NT\bot_ai\strategy\strategy_loader.py
# Purpose: Load and run strategy classes dynamically
# Encoding: UTF-8 without BOM
# ============================================

import importlib
from bot_ai.core.signal import Signal

def load_strategy_class(strategy_name: str):
    """Dynamically import and return the strategy class by name."""
    module_path = f"bot_ai.strategy.{strategy_name}"
    module = importlib.import_module(module_path)
    class_name = "".join(part.capitalize() for part in strategy_name.split("_")) + "Strategy"
    return getattr(module, class_name)

def run_strategy(strategy_name: str, df, params: dict = None) -> Signal | None:
    """Load and run a strategy on the given DataFrame with optional parameters."""
    StrategyClass = load_strategy_class(strategy_name)
    strategy = StrategyClass(params or {})
    return strategy.generate_signal(df, params or {})
