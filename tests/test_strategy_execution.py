# tests/test_strategy_execution.py
# Integration tests for generate_signal() and backtest() methods in RSIReversalStrategy, BreakoutStrategy, and MeanReversionStrategy

import pytest
import pandas as pd
from bot_ai.strategy.rsi_reversal_strategy import RSIReversalStrategy
from bot_ai.strategy.breakout import BreakoutStrategy
from bot_ai.strategy.mean_reversion import MeanReversionStrategy
from bot_ai.core.signal import Signal
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
def test_rsi_generate_signal(mock_log, sample_df):
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
    signal = strategy.generate_signal(df)
    assert signal is None or isinstance(signal, Signal)

@patch("bot_ai.strategy.breakout.log_signal")
def test_breakout_generate_signal(mock_log, sample_df):
    config = {
        "symbol": "BTCUSDT",
        "lookback": 20,
        "take_profit_pct": 0.03,
        "stop_loss_pct": 0.01,
        "max_holding_period": 24
    }
    strategy = BreakoutStrategy(config)
    df = strategy.calculate_indicators(sample_df)
    signal = strategy.generate_signal(df)
    assert signal is None or isinstance(signal, Signal)

@patch("bot_ai.strategy.mean_reversion.log_signal")
def test_mean_reversion_generate_signal(mock_log, sample_df):
    config = {
        "symbol": "BTCUSDT",
        "window": 20,
        "threshold": 0.02,
        "max_holding_period": 24
    }
    strategy = MeanReversionStrategy(config)
    df = strategy.calculate_indicators(sample_df)
    signal = strategy.generate_signal(df)
    assert signal is None or isinstance(signal, Signal)

@patch("bot_ai.strategy.rsi_reversal_strategy.insert_trade")
def test_rsi_backtest(mock_insert, sample_df):
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
    strategy.backtest(df)
    assert isinstance(strategy.trades, list)

@patch("bot_ai.strategy.breakout.insert_trade")
def test_breakout_backtest(mock_insert, sample_df):
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
    strategy.backtest(df)
    assert isinstance(strategy.trades, list)

@patch("bot_ai.strategy.mean_reversion.insert_trade")
def test_mean_reversion_backtest(mock_insert, sample_df):
    config = {
        "symbol": "BTCUSDT",
        "window": 20,
        "threshold": 0.02,
        "max_holding_period": 24
    }
    strategy = MeanReversionStrategy(config)
    df = strategy.calculate_indicators(sample_df)
    df = strategy.generate_signals(df)
    strategy.backtest(df)
    assert isinstance(strategy.trades, list)
