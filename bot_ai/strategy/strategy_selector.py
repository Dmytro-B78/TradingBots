# bot_ai/strategy/strategy_selector.py

from bot_ai.strategy.strategy_loader import load_strategy

class StrategySelector:
    def __init__(self, config):
        self.config = config
        self.strategy_names = config.get("strategies", ["sma"])  # список стратегий по умолчанию

    def select(self, context):
        """
        Перебирает стратегии и возвращает первый сработавший сигнал.
        """
        for name in self.strategy_names:
            strategy = load_strategy(name, self.config)
            signal = strategy.generate_signal(context)
            if signal:
                return signal
        return None

