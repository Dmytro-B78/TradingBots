# tests/test_pipeline_full.py
# Integration test for pipeline with mocked Binance client, strategy, and data

import pytest
import pandas as pd
from bot_ai.selector import pipeline
from bot_ai.selector import pipeline_select_pairs
from bot_ai.strategy.mean_reversion import MeanReversionStrategy
from bot_ai.core.signal import Signal

def test_pipeline_full(monkeypatch, tmp_path):
    # Patch whitelist path to temporary file
    whitelist_file = tmp_path / "whitelist.json"
    whitelist_file.write_text("[]", encoding="utf-8")
    monkeypatch.setattr(pipeline, "_whitelist_path", str(whitelist_file))

    # Patch JSON I/O to avoid file system dependencies
    monkeypatch.setattr(pipeline.json, "load", lambda f: ["AAAUSDT"])
    monkeypatch.setattr(pipeline.json, "dump", lambda obj, f, *a, **k: None)

    # Patch show_top_pairs to no-op
    monkeypatch.setattr(pipeline, "show_top_pairs", lambda cfg, pairs, top_n=2: None)

    # Patch Binance client with mock data
    class MockClient:
        def exchange_info(self):
            return {
                "symbols": [
                    {"symbol": "AAAUSDT", "quoteAsset": "USDT", "status": "TRADING"},
                    {"symbol": "BBBUSDT", "quoteAsset": "USDT", "status": "TRADING"}
                ]
            }

        def ticker_24hr(self):
            return [
                {"symbol": "AAAUSDT", "quoteVolume": "100000", "lastPrice": "85.0", "askPrice": "85.5", "bidPrice": "84.5"},
                {"symbol": "BBBUSDT", "quoteVolume": "50000", "lastPrice": "2.0", "askPrice": "2.02", "bidPrice": "1.98"}
            ]

    monkeypatch.setattr(pipeline_select_pairs, "get_exchange_client", lambda cfg: MockClient())

    # Patch strategy loader to return real MeanReversionStrategy
    monkeypatch.setattr(pipeline, "load_strategy", lambda name, config: MeanReversionStrategy(config))

    # Patch get_data to return synthetic OHLCV data with deviation < -threshold
    def mock_get_data(symbol, interval, lookback, source, **kwargs):
        sma_base = 100
        # 30 candles around 100, then 20 candles dropping from 95 to 85
        prices = [sma_base + (i % 3 - 1) for i in range(30)] + [95 - i * 0.5 for i in range(20)]
        df = pd.DataFrame({
            "time": pd.date_range(start="2026-01-01", periods=50, freq="1h"),
            "open": prices,
            "high": [p + 0.5 for p in prices],
            "low": [p - 0.5 for p in prices],
            "close": prices,
            "volume": [10.0] * 50
        })
        return df

    monkeypatch.setattr(pipeline.pipeline_utils, "get_data", mock_get_data)

    # Patch log_signal to capture emitted signals
    captured_signals = []
    monkeypatch.setattr(pipeline.pipeline_utils, "log_signal", lambda signal, **kwargs: captured_signals.append(signal))

    # Run pipeline
    cfg = {
        "volume_threshold": 100,
        "risk": {"top_n_pairs": 2},
        "strategy": {
            "name": "mean_reversion",
            "params": {
                "window": 20,
                "threshold": 0.02,
                "max_holding_period": 24,
                "symbol": "AAAUSDT"
            }
        },
        "exchange": {
            "apiKey": "test",
            "secret": "test",
            "testnet": True
        }
    }

    result = pipeline.fetch_and_filter_pairs(cfg, use_cache=False)

    # Assertions
    assert result, "Pipeline returned empty result"
    assert isinstance(result, list)
    assert all(isinstance(pair, str) for pair in result)
    assert captured_signals, "No signals were generated or logged"
    assert all(isinstance(sig, Signal) for sig in captured_signals)
