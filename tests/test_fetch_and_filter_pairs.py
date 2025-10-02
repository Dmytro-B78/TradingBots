# tests/test_fetch_and_filter_pairs.py
# Расширенная матрица сценариев с маркерами [CASE] для авто-сводки

import json
import os
import time
import logging
import pytest

@pytest.mark.parametrize("skip_args,expected_pass,description", [
    ({}, False, "Строгая логика, спред > лимита"),
    ({"skip_spread_for": ["FFF/USDT"]}, True, "Пропуск спреда"),
    ({"skip_riskguard_for": ["FFF/USDT"]}, False, "Пропуск RiskGuard, но спред режет"),
    ({"skip_volume_for": ["FFF/USDT"]}, False, "Пропуск объёма, но спред режет"),
    ({"skip_trend_d1_for": ["FFF/USDT"]}, False, "Пропуск тренда D1, но спред режет"),
    ({"skip_trend_ltf_for": ["FFF/USDT"]}, False, "Пропуск тренда LTF, но спред режет"),
    ({"skip_riskguard_for": ["FFF/USDT"], "skip_spread_for": ["FFF/USDT"]}, True, "Пропуск RiskGuard и спреда"),
    ({"skip_volume_for": ["FFF/USDT"], "skip_spread_for": ["FFF/USDT"]}, True, "Пропуск объёма и спреда"),
    ({"skip_trend_d1_for": ["FFF/USDT"], "skip_spread_for": ["FFF/USDT"]}, True, "Пропуск тренда D1 и спреда"),
    ({"skip_trend_ltf_for": ["FFF/USDT"], "skip_spread_for": ["FFF/USDT"]}, True, "Пропуск тренда LTF и спреда"),
    ({
        "skip_riskguard_for": ["FFF/USDT"],
        "skip_volume_for": ["FFF/USDT"],
        "skip_spread_for": ["FFF/USDT"],
        "skip_trend_d1_for": ["FFF/USDT"],
        "skip_trend_ltf_for": ["FFF/USDT"]
    }, True, "Пропуск всех фильтров"),
])
def test_fetch_and_filter_pairs_matrix(monkeypatch, tmp_path, caplog, skip_args, expected_pass, description):
    """
    Параметризованный тест всех веток fetch_and_filter_pairs для FFF/USDT
    с разными комбинациями отключённых фильтров.
    """
    from bot_ai.selector.pipeline import fetch_and_filter_pairs

    caplog.set_level(logging.INFO)

    # --- Маркер сценария для авто-сводки ---
    print(f"[CASE] {description} | expected_pass={expected_pass} | skip_args={skip_args}")

    # --- Свежий кэш ---
    cache_file = tmp_path / "whitelist.json"
    pairs_in_cache = ["AAA/USDT"]
    cache_file.write_text(json.dumps(pairs_in_cache), encoding="utf-8")
    os.makedirs("data", exist_ok=True)
    os.replace(cache_file, "data/whitelist.json")
    monkeypatch.setattr("bot_ai.selector.pipeline.os.path.getmtime", lambda f: time.time())
    monkeypatch.setattr("bot_ai.selector.pipeline.show_top_pairs", lambda cfg, pairs, top_n=5: None)

    # --- Устаревший кэш + фильтры ---
    monkeypatch.setattr("bot_ai.selector.pipeline.os.path.getmtime", lambda f: time.time() - 100000)

    class DummyExchange:
        def __init__(self, *a, **k): pass
        def load_markets(self):
            return {
                "AAA/USDT": {"active": True},
                "BBB/USDT": {"active": True},
                "CCC/USDT": {"active": True},
                "DDD/USDT": {"active": True},
                "EEE/USDT": {"active": True},
                "FFF/USDT": {"active": True}
            }
        def fetch_ticker(self, symbol):
            if symbol == "EEE/USDT":
                raise Exception("ticker fail")
            if symbol == "AAA/USDT":
                return {"quoteVolume": 50, "ask": 1.1, "bid": 1.0}
            if symbol == "BBB/USDT":
                return {"quoteVolume": 1000, "ask": 2.0, "bid": 1.0}
            if symbol == "CCC/USDT":
                return {"quoteVolume": 1000, "ask": 1.1, "bid": 1.0}
            if symbol == "DDD/USDT":
                return {"quoteVolume": 1000, "ask": 1.1, "bid": 1.0}
            if symbol == "FFF/USDT":
                return {"quoteVolume": 1000, "ask": 1.1, "bid": 1.0}
            return {}
        def fetch_ohlcv(self, symbol, timeframe, limit):
            if symbol.upper() == "FFF/USDT":
                slow = limit
                fast = max(1, slow - 1)
                length = max(limit, slow + 1)
                closes = [1.0] * (length - slow) + [1.5] * (slow - fast) + [2.0] * fast
                return [[0,0,0,0,c,0] for c in closes]
            if symbol == "CCC/USDT" and timeframe == "1d":
                raise Exception("trend fail D1")
            if symbol == "DDD/USDT" and timeframe == "1h":
                raise Exception("trend fail LTF")
            closes = [1.0] * limit
            return [[0,0,0,0,c,0] for c in closes]

    monkeypatch.setattr("bot_ai.selector.pipeline.ccxt.binance", DummyExchange)

    class DummyRG:
        def can_open_trade(self, symbol):
            return symbol != "AAA/USDT"

    cfg_full = type("Cfg", (), {
        "exchange": "binance",
        "risk": type("Risk", (), {"min_24h_volume_usdt": 100, "max_spread_pct": 5}),
        "pair_selection": {
            "d1_timeframe": "1d", "d1_sma_fast": 1, "d1_sma_slow": 2,
            "ltf_timeframe": "1h", "ltf_sma_fast": 1, "ltf_sma_slow": 2
        }
    })

    caplog.clear()
    result = fetch_and_filter_pairs(cfg_full, risk_guard=DummyRG(), use_cache=True, cache_ttl_hours=0, **skip_args)
    if expected_pass:
        assert "FFF/USDT" in result, f"{description}: ожидали прохождение, но пара отсутствует"
    else:
        assert "FFF/USDT" not in result, f"{description}: ожидали отсеивание, но пара присутствует"
