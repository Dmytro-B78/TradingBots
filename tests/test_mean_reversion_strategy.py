import pytest
import pandas as pd
from bot_ai.strategy.mean_reversion import MeanReversionStrategy

@pytest.fixture
def sample_df():
    data = {
        "time": pd.date_range(start="2026-01-01", periods=40, freq="1h"),
        "open": [100 + i for i in range(40)],
        "high": [101 + i for i in range(40)],
        "low": [99 + i for i in range(40)],
        "close": [100 + i for i in range(20)] + [120 - i for i in range(20)],
        "volume": [10.0] * 40
    }
    return pd.DataFrame(data)

def test_mean_reversion_strategy_generate_signals(sample_df):
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
    assert df["signal"].isin(["BUY", "SELL", None]).all()
