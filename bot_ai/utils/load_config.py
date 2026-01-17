# -*- coding: utf-8 -*-
# ============================================
# File: bot_ai/utils/load_config.py
# Назначение: Загрузка конфигурации из config.json с поддержкой BOM
# ============================================

import json
import os

def load_config() -> dict:
    """
    Загружает конфигурацию из config.json, поддерживает UTF-8 с BOM.
    """
    config_path = os.path.join(os.path.dirname(__file__), "..", "..", "config.json")
    try:
        with open(config_path, "r", encoding="utf-8-sig") as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Ошибка при загрузке config.json: {e}")
        return {}
