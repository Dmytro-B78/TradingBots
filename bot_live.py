# -*- coding: utf-8 -*-
# ============================================
# 📂 File: bot_live.py
# 🪵 Назначение: Прогон стратегий с логированием
# ============================================

import os
import json
import logging
from datetime import datetime
from bot_ai.strategy import strategy_selector
from bot_ai.loaders.sample_data import load_sample_data

# 📁 Создаём папку logs, если её нет
os.makedirs("logs", exist_ok=True)

# 🕒 Имя лог-файла с меткой времени
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
log_file = os.path.join("logs", f"bot_live_{timestamp}.log")

# 🪵 Настройка логгера
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="[{asctime}] [{levelname}] {message}",
    style="{"
)

def log(msg, level="info"):
    print(msg)
    getattr(logging, level)(msg)

def main():
    log("🚀 Тестирование выбранных стратегий...\n")

    strategy_files = [
        "range",
        "volatile",
        "rsi_macd",
        "rsi_bbands",
        "rsi_ichimoku"
    ]

    df = load_sample_data()

    for name in strategy_files:
        log(f"🔍 Тест стратегии: {name}")
        try:
            config_path = os.path.join("bot_ai", "config", f"{name}.json")
            with open(config_path, "r", encoding="utf-8-sig") as f:
                config = json.load(f)

            strategy = strategy_selector.get_strategy(name, config)
            strategy.load_data(df)
            strategy.generate_signals()
            result = strategy.run_backtest()
            log(f"✅ Результат: {result}")

            if hasattr(strategy, "summary"):
                summary = strategy.summary()
                log(f"📊 Статистика: {summary}")
        except Exception as e:
            log(f"❌ Ошибка в [{name}]: {e}", level="error")
        log("")

if __name__ == "__main__":
    main()
