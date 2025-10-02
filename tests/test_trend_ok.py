import pandas as pd
import pytest

def test_trend_ok_all_branches(monkeypatch):
    """
    Полный тест всех веток _trend_ok:
    - SMA_fast > SMA_slow → True
    - SMA_fast <= SMA_slow → False
    - Исключение → False
    """
    from bot_ai.selector.pipeline import _trend_ok

    # Dummy exchange для успешного тренда
    class ExchangeGood:
        def fetch_ohlcv(self, symbol, timeframe, limit):
            closes = [1.0] * (limit - 1) + [2.0]  # fast > slow
            return [[0,0,0,0,c,0] for c in closes]

    # Dummy exchange для плохого тренда
    class ExchangeBad:
        def fetch_ohlcv(self, symbol, timeframe, limit):
            closes = [1.0] * limit  # fast == slow
            return [[0,0,0,0,c,0] for c in closes]

    # Dummy exchange для исключения
    class ExchangeFail:
        def fetch_ohlcv(self, symbol, timeframe, limit):
            raise Exception("fail")

    # 1. Успешный тренд
    assert _trend_ok(ExchangeGood(), "AAA/USDT", tf="1d", fast=1, slow=2) == True

    # 2. Плохой тренд
    assert _trend_ok(ExchangeBad(), "AAA/USDT", tf="1d", fast=1, slow=2) == False

    # 3. Исключение
    assert _trend_ok(ExchangeFail(), "AAA/USDT", tf="1d", fast=1, slow=2) == False
