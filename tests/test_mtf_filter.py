import pandas as pd
from bot_ai.filters import mtf_filter

# Проверяет, что apply_mtf_filter возвращает DataFrame
def test_apply_mtf_filter_returns_dataframe():
    signal_df = pd.DataFrame({
        "timestamp": ["2024-01-01 00:00:00", "2024-01-01 00:01:00"],
        "symbol": ["BTCUSDT", "ETHUSDT"],
        "signal": [True, True]
    })

    timeframe_data = {
        "1h": pd.DataFrame({
            "timestamp": ["2024-01-01 00:00:00", "2024-01-01 00:01:00"],
            "symbol": ["BTCUSDT", "ETHUSDT"],
            "trend": ["up", "down"]
        })
    }

    config = {
        "enabled": True,
        "required_trend": "up"
    }

    result = mtf_filter.apply_mtf_filter(signal_df, timeframe_data, config)

    assert isinstance(result, pd.DataFrame)
    assert len(result) == 1
    assert result.iloc[0]["symbol"] == "BTCUSDT"
