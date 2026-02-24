# -*- coding: utf-8 -*-
# ============================================
# Файл: bot_ai/selector/pipeline.py
# Назначение: Отбор торговых пар и сохранение whitelist
# ============================================

import os
import json
import logging
import argparse
import yaml
import ccxt

# Импорты из соседних модулей
from .pipeline_select_pairs import select_pairs
from .pipeline_show_fix import show_top_pairs
from . import pipeline_utils
from . import filters
from . import metrics
from . import trend_utils

# Путь к файлу whitelist
_whitelist_path = "data/whitelist.json"

# === Основная функция отбора пар ===
def fetch_and_filter_pairs(cfg, use_cache=True, cache_ttl_hours=24):
    if use_cache and os.path.exists(_whitelist_path):
        logging.info("[CACHE] Загрузка whitelist из файла")
        with open(_whitelist_path, "r", encoding="utf-8") as f:
            whitelist = json.load(f)
        return whitelist

    logging.info("[CACHE] Кэш не используется или файл отсутствует — пересчёт")
    pairs = select_pairs(cfg)
    logging.info(f"[DEBUG] Отобрано пар: {len(pairs)}")

    show_top_pairs(cfg, pairs)

    whitelist = [p["pair"] for p in pairs]
    os.makedirs(os.path.dirname(_whitelist_path), exist_ok=True)
    with open(_whitelist_path, "w", encoding="utf-8") as f:
        json.dump(whitelist, f, indent=2, ensure_ascii=False)

    logging.info(f"✅ Сохранено {len(whitelist)} пар в {_whitelist_path}")
    return whitelist

# === Обёртка для внешнего вызова ===
def run_pipeline(cfg):
    return fetch_and_filter_pairs(cfg)

# === CLI-запуск ===
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, required=True)
    parser.add_argument("--mode", type=str, default="paper")
    parser.add_argument("--log-level", type=str, default="INFO")
    args = parser.parse_args()

    # Настройка логгера: консоль + файл, UTF-8
    log_level = getattr(logging, args.log_level.upper(), logging.INFO)
    log_format = "%(asctime)s [%(levelname)s] %(message)s"
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)

    logging.basicConfig(
        level=log_level,
        format=log_format,
        handlers=[
            logging.FileHandler(f"{log_dir}/pipeline.log", encoding="utf-8"),
            logging.StreamHandler()
        ]
    )

    logging.info(f"🚀 Запуск pipeline в режиме {args.mode}")

    with open(args.config, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    cfg["mode"] = args.mode

    whitelist = fetch_and_filter_pairs(cfg)
    logging.info(f"🎯 Финальный whitelist: {whitelist}")

# Поддержка запуска через `python -m bot_ai.selector.pipeline`
if __name__ == "__main__" or __name__.endswith(".pipeline"):
    main()
