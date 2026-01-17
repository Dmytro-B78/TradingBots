# -*- coding: utf-8 -*-
# ============================================
# File: tests/test_smoke.py
# Назначение: Проверка базовой работоспособности проекта
# ============================================

from config.config_loader import get_binance_credentials

def test_credentials_loaded():
    """
    Проверяет, что ключи Binance успешно загружаются из .env
    """
    api_key, api_secret = get_binance_credentials()
    assert api_key is not None and len(api_key) > 0
    assert api_secret is not None and len(api_secret) > 0
