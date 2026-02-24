# -*- coding: utf-8 -*-
# ============================================
# File: run_optimize.py
# Назначение: Запуск отбора пар и оптимизации
# Структура: CLI-обёртка, логирование, конфигурация, пайплайн + grid search
# ============================================

import os
import json
import logging
from datetime import datetime

from bot_ai.selector.pipeline import run_pipeline
from bot_ai.optimize import run_grid_search, optimize_breakout_window
from bot_ai.selector.filters import get_exchange_client

# === Настройка логирования ===
def setup_logger():
    os.makedirs("logs", exist_ok=True)
    log_path = os.path.join("logs", "optimize.log")
    logging.basicConfig(
        filename=log_path,
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        encoding="utf-8"
    )
    logging.getLogger().addHandler(logging.StreamHandler())
    logging.info("=== Запуск run_optimize.py ===")
    logging.info(f"Лог сохраняется в {log_path}")

# === Загрузка конфигурации с поддержкой BOM ===
def load_config(path="config.json"):
    with open(path, "r", encoding="utf-8-sig") as f:
        return json.load(f)

# === Оптимизация стратегии breakout по окну ===
def run_breakout_optimization(cfg):
    exchange_client = get_exchange_client(cfg)
    timeframe = cfg["backtest"].get("timeframe", "15m")
    limit = cfg["backtest"].get("lookback_bars", 500)
    window_range = cfg["optimize"].get("breakout_window_range", list(range(5, 31)))

    with open("data/whitelist.json", "r", encoding="utf-8") as f:
        symbols = json.load(f)

    results = []
    for symbol in symbols:
        try:
            ohlcv = exchange_client.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
            candles = [
                {"timestamp": o[0], "open": o[1], "high": o[2], "low": o[3], "close": o[4], "volume": o[5]}
                for o in ohlcv
            ]
            result = optimize_breakout_window(symbol, candles, window_range)
            if result:
                results.append(result)
        except Exception as e:
            logging.warning(f"[ERROR] {symbol}: {e}")

    os.makedirs("results", exist_ok=True)
    with open("results/best_breakout_windows.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    logging.info(f"[SAVE] Сохранены лучшие окна breakout для {len(results)} пар в results/best_breakout_windows.json")

# === Основной запуск ===
def main():
    setup_logger()
    cfg = load_config()

    # Шаг 1: Отбор пар
    logging.info("🚀 Шаг 1: Отбор пар по фильтрам")
    run_pipeline(cfg)

    # Шаг 2: Grid Search оптимизация mean_reversion
    logging.info("⚙️  Шаг 2: Grid Search оптимизация mean_reversion")
    run_grid_search(cfg)

    # Шаг 3: Оптимизация breakout
    logging.info("📈 Шаг 3: Оптимизация стратегии breakout")
    run_breakout_optimization(cfg)

    logging.info("🏁 Оптимизация завершена")

if __name__ == "__main__":
    main()
