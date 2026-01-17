# -*- coding: utf-8 -*-
# ============================================
# File: bot_ai/config/config_loader.py
# Назначение: Загрузка API-ключей и конфигурации стратегии
# ============================================

import os
import json
from dotenv import load_dotenv

# === Путь к .env в корне проекта ===
env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))
load_dotenv(dotenv_path=env_path)

def get_binance_credentials():
    """
    Возвращает API-ключ и секрет из .env.
    """
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")
    return api_key, api_secret

def load_config():
    """
    Загружает config.json из корня проекта.
    Поддерживает UTF-8 с BOM (utf-8-sig).
    """
    config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "config.json"))
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Файл конфигурации не найден: {config_path}")
    with open(config_path, "r", encoding="utf-8-sig") as f:
        return json.load(f)
