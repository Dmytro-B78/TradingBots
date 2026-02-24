# tests/test_pipeline.py

import builtins
import json
from types import SimpleNamespace

from bot_ai.selector import pipeline
from bot_ai.selector import pipeline_select_pairs

class DummyExchange:
    def __init__(self):
        self.markets = {
            "BTC/USDT": {"active": True},
            "ETH/USDT": {"active": True}
        }

    def load_markets(self):
        return self.markets

    def fetch_ticker(self, symbol):
        return {
            "quoteVolume": 2000000,
            "ask": 100.1,
            "bid": 100.0,
            "last": 100.05,
            "high": 101.0,
            "low": 99.0,
            "close": 100.05
        }

    def fetch_ohlcv(self, symbol, timeframe, limit):
        closes = [100 + (i * 0.1) for i in range(limit)]
        return [[None, None, None, None, c, None] for c in closes]

def make_cfg():
    return SimpleNamespace(
        exchange="binance",
        risk=SimpleNamespace(
            min_24h_volume_usdt=1000000,
            max_spread_pct=10.0,
            test_equity=1000
        ),
        pair_selection={
            "d1_timeframe": "1d",
            "d1_sma_fast": 2,
            "d1_sma_slow": 3,
            "ltf_timeframe": "1h",
            "ltf_sma_fast": 2,
            "ltf_sma_slow": 3
        }
    )

def test_select_pairs_no_cache(monkeypatch, tmp_path):
    cfg = make_cfg()
    monkeypatch.setattr(pipeline.ccxt, "binance", lambda *a, **k: DummyExchange())
    monkeypatch.setattr(pipeline, "show_top_pairs", lambda *a, **k: None)
    monkeypatch.setattr(pipeline.os, "makedirs", lambda *a, **k: None)
    monkeypatch.setattr(pipeline.os.path, "exists", lambda p: False)
    monkeypatch.setattr("builtins.open", lambda *a, **k: open(*a, **k))
    monkeypatch.setattr(pipeline.json, "dump", lambda obj, f, *a, **k: None)
    monkeypatch.setattr(pipeline_select_pairs, "detect_regime", lambda *a, **k: "uptrend")

    result = pipeline.select_pairs(cfg, risk_guard=None)
    print("RESULT:", result)
    assert isinstance(result, list)
    assert any(p["pair"] in ["BTC/USDT", "ETH/USDT"] for p in result)

def test_select_pairs_with_cache(monkeypatch, tmp_path):
    cfg = make_cfg()
    whitelist_file = tmp_path / "whitelist.json"
    whitelist_file.write_text(json.dumps(["BTC/USDT"]), encoding="utf-8")

    real_open = open
    real_json_load = json.load

    monkeypatch.setattr(pipeline, "_whitelist_path", str(whitelist_file))
    monkeypatch.setattr(pipeline.os.path, "exists", lambda p: True)
    monkeypatch.setattr("builtins.open", lambda *a, **k: real_open(*a, **k))
    monkeypatch.setattr(pipeline.json, "load", lambda f: real_json_load(f))
    monkeypatch.setattr(pipeline, "show_top_pairs", lambda *a, **k: None)
    monkeypatch.setattr(pipeline.ccxt, "binance", lambda *a, **k: DummyExchange())

    result = pipeline.fetch_and_filter_pairs(cfg, use_cache=True, cache_ttl_hours=24)
    print("CACHED RESULT:", result)
    assert result == ["BTC/USDT"]
# Добавим в конец tests/test_pipeline.py

def test_show_top_pairs_logs_volume(monkeypatch):
    cfg = make_cfg()

    class MockExchange:
        def fetch_ticker(self, symbol):
            return {"quoteVolume": 123456.78}

    logs = []

    monkeypatch.setattr(pipeline_show_fix, "ccxt", SimpleNamespace(binance=lambda: MockExchange()))
    monkeypatch.setattr(pipeline_show_fix, "logger", SimpleNamespace(info=lambda msg: logs.append(msg)))

    pairs = ["BTC/USDT", "ETH/USDT"]
    result = pipeline_show_fix.show_top_pairs(cfg, pairs)

    print("LOGS:", logs)
    assert any("BTC/USDT" in log and "volume=123456.78" in log for log in logs)
    assert any("ETH/USDT" in log and "volume=123456.78" in log for log in logs)
    assert result is False
# Добавим в начало файла (рядом с другими импортами)

from bot_ai.selector import pipeline_show_fix
# Добавим в конец tests/test_pipeline.py

def test_pipeline_end_to_end(monkeypatch, tmp_path):
    cfg = make_cfg()
    whitelist_file = tmp_path / "whitelist.json"

    class MockExchange:
        def __init__(self):
            self.markets = {
                "BTC/USDT": {"active": True},
                "ETH/USDT": {"active": True},
                "XRP/USDT": {"active": True}
            }

        def load_markets(self):
            return self.markets

        def fetch_ticker(self, symbol):
            return {
                "quoteVolume": 2_000_000,
                "ask": 100.1,
                "bid": 100.0,
                "last": 100.05,
                "high": 101.0,
                "low": 99.0,
                "close": 100.05
            }

        def fetch_ohlcv(self, symbol, timeframe, limit):
            closes = [100 + (i * 0.1) for i in range(limit)]
            return [[None, None, None, None, c, None] for c in closes]

    monkeypatch.setattr(pipeline, "_whitelist_path", str(whitelist_file))
    monkeypatch.setattr(pipeline.ccxt, "binance", lambda *a, **k: MockExchange())
    monkeypatch.setattr(pipeline_select_pairs, "detect_regime", lambda *a, **k: "uptrend")
    monkeypatch.setattr(pipeline, "show_top_pairs", lambda *a, **k: None)

    result = pipeline.fetch_and_filter_pairs(cfg, use_cache=False)
    print("END-TO-END RESULT:", result)

    assert isinstance(result, list)
    assert "BTC/USDT" in result
    assert "ETH/USDT" in result
    assert whitelist_file.exists()
