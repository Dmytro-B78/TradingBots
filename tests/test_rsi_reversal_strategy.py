import pytest
import pandas as pd
from bot_ai.strategy.rsi_reversal_strategy import RSIReversalStrategy

@pytest.fixture
def sample_df():
    data = {
        "time": pd.date_range(start="2026-01-01", periods=20, freq="1h"),
        "open": [100 + i for i in range(20)],
        "high": [101 + i for i in range(20)],
        "low": [99 + i for i in range(20)],
        "close": [100 + i for i in range(10)] + [90 - i for i in range(10)],
        "volume": [10.0] * 20
    }
    return pd.DataFrame(data)

def test_rsi_reversal_strategy_generate_signals(sample_df):
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
    assert df["signal"].isin(["BUY", "SELL", None]).all()
