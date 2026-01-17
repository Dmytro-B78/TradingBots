# -*- coding: utf-8 -*-
# ============================================
# File: tests/test_backtest_engine.py
# Назначение: Тесты для backtest_engine
# ============================================

import pandas as pd
import pytest
from unittest.mock import patch

from backtest.backtest_engine import run_backtest

# === Заглушка для стратегии ===

def dummy_strategy(pair, df, config):
    return [{
        "timestamp": df.index[-1].isoformat() if not df.empty else "n/a",
        "side": "BUY",
        "price": df["close"].iloc[-1] if not df.empty else 0
    }]

# === Тест с подменой fetch_ohlcv и select_strategy ===

@patch("backtest.backtest_engine.fetch_ohlcv")
@patch("backtest.backtest_engine.select_strategy")
def test_run_backtest_basic(mock_select_strategy, mock_fetch_ohlcv, capsys):
    # Подготовка данных
    df = pd.DataFrame({
        "open": [1, 2, 3, 4, 5],
        "high": [2, 3, 4, 5, 6],
        "low": [0, 1, 2, 3, 4],
        "close": [1.5, 2.5, 3.5, 4.5, 5.5],
        "volume": [100, 200, 300, 400, 500]
    }, index=pd.date_range("2023-01-01", periods=5, freq="1h"))

    mock_fetch_ohlcv.return_value = df
    mock_select_strategy.return_value = dummy_strategy

    config = {
        "strategy": "adaptive",
        "symbol": "BTCUSDT",
        "timeframe": "1h"
    }

    run_backtest(config["symbol"], config["strategy"], config["timeframe"], config)

    captured = capsys.readouterr()
    assert "[BACKTEST] ▶ BTCUSDT" in captured.out
    assert "Сигналов: 1" in captured.out
    assert "BUY" in captured.out
