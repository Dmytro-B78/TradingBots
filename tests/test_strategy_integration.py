# tests/test_strategy_integration.py
# Integration tests for RSIReversalStrategy, BreakoutStrategy, and MeanReversionStrategy
# Verifies indicator calculation, signal generation, and logging

import pytest
import pandas as pd
from bot_ai.strategy.rsi_reversal_strategy import RSIReversalStrategy
from bot_ai.strategy.breakout import BreakoutStrategy
from bot_ai.strategy.mean_reversion import MeanReversionStrategy
from unittest.mock import patch

@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "time": pd.date_range(start="2026-01-01", periods=50, freq="1h"),
        "open": [100 + i for i in range(50)],
        "high": [101 + i for i in range(50)],
        "low": [99 + i for i in range(50)],
        "close": [100 + i for i in range(25)] + [120 - i for i in range(25)],
        "volume": [10.0] * 50
    })

@patch("bot_ai.strategy.rsi_reversal_strategy.log_signal")
def test_rsi_reversal_integration(mock_log, sample_df):
    config = {
        "symbol": "BTCUSDT",
        "rsi_period": 14,
        "rsi_oversold": 30,
        "rsi_overbought": 70,
        "take_profit_pct": 0.02,
        "trailing_stop_pct": 0.015,
        "max_holding_period": 24
    }
    strategy = RSIReversalStrategy(config)
    df = strategy.calculate_indicators(sample_df)
    df = strategy.generate_signals(df)

    assert "signal" in df.columns
    print("RSI signals:", df["signal"].value_counts(dropna=False))
    assert mock_log.called

@patch("bot_ai.strategy.breakout.log_signal")
def test_breakout_integration(mock_log, sample_df):
    config = {
        "symbol": "BTCUSDT",
        "lookback": 20,
        "take_profit_pct": 0.03,
        "stop_loss_pct": 0.01,
        "max_holding_period": 24
    }
    strategy = BreakoutStrategy(config)
    df = strategy.calculate_indicators(sample_df)
    df = strategy.generate_signals(df)

    assert "signal" in df.columns
    print("Breakout signals:", df["signal"].value_counts(dropna=False))
    assert mock_log.called

@patch("bot_ai.strategy.mean_reversion.log_signal")
def test_mean_reversion_integration(mock_log, sample_df):
    config = {
        "symbol": "BTCUSDT",
        "window": 20,
        "threshold": 0.02,
        "max_holding_period": 24
    }
    strategy = MeanReversionStrategy(config)
    df = strategy.calculate_indicators(sample_df)
    df = strategy.generate_signals(df)

    assert "signal" in df.columns
    print("Mean Reversion signals:", df["signal"].value_counts(dropna=False))
    assert mock_log.called
