# strategy_loader.py
# Назначение: Загрузка всех стратегий из папки strategy/
# Структура:
# └── bot_ai/strategy/strategy_loader.py

import os
import importlib.util

def load_strategies(config, strategy_dir="bot_ai/strategy"):
    strategies = []

    for filename in os.listdir(strategy_dir):
        if filename.endswith(".py") and not filename.startswith("__"):
            path = os.path.join(strategy_dir, filename)
            name = os.path.splitext(filename)[0]

            spec = importlib.util.spec_from_file_location(name, path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            if hasattr(module, "generate_signal"):
                strategies.append({
                    "name": name,
                    "fn": module.generate_signal
                })

    return strategies
