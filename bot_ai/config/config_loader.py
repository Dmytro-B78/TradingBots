# -*- coding: utf-8 -*-
# ============================================
# File: bot_ai/config/config_loader.py
# Назначение: Загрузка конфигурации из YAML-файла и .env
# Используется в run_strategies.py и других модулях
# ============================================

import os
import yaml
from dotenv import load_dotenv

# === Загрузка переменных окружения из .env ===
env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))
load_dotenv(dotenv_path=env_path)

def get_binance_credentials():
    """
    Возвращает API-ключи Binance из .env
    """
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")
    return api_key, api_secret

def load_config(path="bot_ai/config/default_config.yaml"):
    """
    Загружает YAML-конфигурацию из указанного пути.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Файл конфигурации не найден: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)
