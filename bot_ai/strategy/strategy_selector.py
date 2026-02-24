# ============================================
# File: bot_ai/strategy/strategy_selector.py
# Purpose: StrategySelector class and default instance
# Format: UTF-8 without BOM
# Compatible with paper_trader and router
# ============================================

from bot_ai.strategy.strategy_loader import load_strategy

class StrategySelector:
    def __init__(self, config):
        self.config = config
        self.strategy_names = config.get("strategies", ["sma"])

    def select(self, context):
        df = context["df"]
        for name in self.strategy_names:
            strategy_class = load_strategy(name)
            instance = strategy_class(self.config)
            signal = instance.generate_signal(df)  # <-- FIXED: only df passed
            if signal:
                return signal
        return None

# === Default selector instance for compatibility ===
strategy_selector = StrategySelector(config={})
