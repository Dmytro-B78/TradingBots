# -*- coding: utf-8 -*-
# ============================================
# File: bot_ai/cli/optimize_cli.py
# Назначение: CLI-интерфейс для запуска Grid Search оптимизации
# Использует: bot_ai.optimize.run_grid_search
# ============================================

import argparse
import json
import logging
from bot_ai.optimize import run_grid_search

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

def load_config(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    parser = argparse.ArgumentParser(description="🚀 Grid Search оптимизация параметров стратегии")
    parser.add_argument("--config", type=str, default="config.json", help="Путь к конфигурационному файлу")
    args = parser.parse_args()

    setup_logging()
    config = load_config(args.config)

    logging.info(f"[START] Запуск оптимизации с конфигом: {args.config}")
    run_grid_search(config)

if __name__ == "__main__":
    main()
