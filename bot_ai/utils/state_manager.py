# -*- coding: utf-8 -*-
# === bot_ai/utils/state_manager.py ===
# Управление состоянием между запусками: загрузка и сохранение state.json

import json
import logging
import os

# === Путь к файлу состояния ===
STATE_PATH = "state.json"

# === Загрузка состояния из файла ===

def load_state():
    if not os.path.exists(STATE_PATH):
        logging.info(
            "[STATE] ?? Файл состояния не найден — создаём пустое состояние")
        return {}
    try:
        with open(STATE_PATH, "r", encoding="utf-8") as f:
            state = json.load(f)
            logging.info("[STATE] ? Состояние загружено")
            return state
    except Exception as e:
        logging.error(f"[STATE] ? Ошибка загрузки состояния: {e}")
        return {}

# === Сохранение состояния в файл ===

def save_state(state: dict):
    try:
        with open(STATE_PATH, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
            logging.info("[STATE] ?? Состояние сохранено")
    except Exception as e:
        logging.error(f"[STATE] ? Ошибка сохранения состояния: {e}")

