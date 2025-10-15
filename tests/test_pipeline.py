import pytest
import json
import builtins
from types import SimpleNamespace
from bot_ai.selector import pipeline

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
            "bid": 100.0
        }
    def fetch_ohlcv(self, symbol, timeframe, limit):
        closes = [100 + (i * 0.1) for i in range(limit)]
        return [[None, None, None, None, c, None] for c in closes]

def make_cfg():
    return SimpleNamespace(
        exchange="binance",
        risk=SimpleNamespace(
            min_24h_volume_usdt=1000000,
            max_spread_pct=10.0
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

    whitelist_file = tmp_path / "whitelist.json"
    real_open = builtins.open
    def fake_open(path, mode="r", *a, **k):
        if isinstance(path, str) and "whitelist.json" in path:
            return real_open(whitelist_file, mode, *a, **k)
        return real_open(path, mode, *a, **k)
    monkeypatch.setattr("builtins.open", fake_open)
    monkeypatch.setattr(pipeline.json, "dump", lambda obj, f, *a, **k: None)

    result = pipeline.select_pairs(cfg, risk_guard=None)
    assert isinstance(result, list)
    assert "BTC/USDT" in result or "ETH/USDT" in result

def test_select_pairs_with_cache(monkeypatch, tmp_path):
    cfg = make_cfg()
    whitelist_file = tmp_path / "whitelist.json"
    whitelist_file.write_text(json.dumps(["BTC/USDT"]), encoding="utf-8")

    monkeypatch.setattr(pipeline, "_whitelist_path", lambda: str(whitelist_file))
    real_open = builtins.open
    def fake_open(path, mode="r", *a, **k):
        if isinstance(path, str) and "whitelist.json" in path:
            return real_open(whitelist_file, mode, *a, **k)
        return real_open(path, mode, *a, **k)
    monkeypatch.setattr("builtins.open", fake_open)
    monkeypatch.setattr(pipeline.json, "load", lambda f: ["BTC/USDT"])
    monkeypatch.setattr(pipeline.os.path, "exists", lambda p: True)
    monkeypatch.setattr(pipeline.os.path, "getmtime", lambda p: pipeline.time.time())
    monkeypatch.setattr(pipeline, "show_top_pairs", lambda *a, **k: None)
    monkeypatch.setattr(pipeline.ccxt, "binance", lambda *a, **k: DummyExchange())

    result = pipeline.fetch_and_filter_pairs(cfg, use_cache=True, cache_ttl_hours=24)
    assert result == ["BTC/USDT"]
