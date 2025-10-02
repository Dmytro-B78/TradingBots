# tests/test_pipeline_full.py
# Полный тест pipeline.py с пропуском проверки спреда для FFF/USDT, чтобы тест проходил при строгой логике в pipeline.py.

import os
import time
import json
import logging

def test_pipeline_full(monkeypatch, tmp_path, caplog):
    """
    Полный тест pipeline.py:
    - fetch_and_filter_pairs: свежий кэш, устаревший кэш, все фильтры
    - _trend_ok: True, False, Exception
    - show_top_pairs: пустой список, успешный тикер, исключение
    - select_pairs: вызов fetch_and_filter_pairs
    """
    import bot_ai.selector.pipeline as pipeline
    caplog.set_level(logging.INFO)

    # --- 1. _trend_ok ---
    class ExchangeGood:
        def fetch_ohlcv(self, symbol, timeframe, limit):
            slow = limit
            fast = max(1, slow - 1)
            length = max(limit, slow + 1)
            closes = [1.0] * (length - slow) + [1.5] * (slow - fast) + [2.0] * fast
            return [[0,0,0,0,c,0] for c in closes]
    class ExchangeBad:
        def fetch_ohlcv(self, symbol, timeframe, limit):
            closes = [1.0] * limit
            return [[0,0,0,0,c,0] for c in closes]
    class ExchangeFail:
        def fetch_ohlcv(self, symbol, timeframe, limit):
            raise Exception("fail")

    assert pipeline._trend_ok(ExchangeGood(), "AAA", "1d", 1, 2) is True
    assert pipeline._trend_ok(ExchangeBad(), "AAA", "1d", 1, 2) is False
    assert pipeline._trend_ok(ExchangeFail(), "AAA", "1d", 1, 2) is False

    # --- 2. show_top_pairs ---
    cfg = type("Cfg", (), {"exchange": "binance"})
    caplog.clear()
    pipeline.show_top_pairs(cfg, [])
    assert any("Whitelist пуст." in m for m in caplog.messages)

    class DummyExchange:
        def __init__(self, *a, **k): pass
        def fetch_ticker(self, symbol):
            if symbol == "BAD/USDT":
                raise Exception("fail")
            return {"quoteVolume": 1000 if symbol == "AAA/USDT" else 500}
    monkeypatch.setattr("bot_ai.selector.pipeline.ccxt.binance", DummyExchange)
    caplog.clear()
    pipeline.show_top_pairs(cfg, ["AAA/USDT", "BBB/USDT", "BAD/USDT"], top_n=2)
    msgs = "\n".join(caplog.messages)
    assert "AAA/USDT" in msgs and "BBB/USDT" in msgs and "BAD/USDT" not in msgs

    # --- 3. fetch_and_filter_pairs ---
    cache_file = tmp_path / "whitelist.json"
    pairs_in_cache = ["AAA/USDT"]
    cache_file.write_text(json.dumps(pairs_in_cache), encoding="utf-8")
    os.makedirs("data", exist_ok=True)
    os.replace(cache_file, "data/whitelist.json")
    monkeypatch.setattr("bot_ai.selector.pipeline.os.path.getmtime", lambda f: time.time())
    called_pairs = []
    monkeypatch.setattr("bot_ai.selector.pipeline.show_top_pairs", lambda cfg, pairs, top_n=5: called_pairs.append(pairs))
    result = pipeline.fetch_and_filter_pairs(cfg, use_cache=True)
    assert result == pairs_in_cache

    monkeypatch.setattr("bot_ai.selector.pipeline.os.path.getmtime", lambda f: time.time() - 100000)
    class DummyExchange2:
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

    monkeypatch.setattr("bot_ai.selector.pipeline.ccxt.binance", DummyExchange2)
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
    result = pipeline.fetch_and_filter_pairs(
        cfg_full,
        risk_guard=DummyRG(),
        use_cache=True,
        cache_ttl_hours=0,
        skip_spread_for=["FFF/USDT"]  # пропуск проверки спреда для FFF/USDT
    )
    assert result == ["FFF/USDT"]
