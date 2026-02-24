import pandas as pd
import pytest

def test_dynamic_sltp_all_branches():
    from bot_ai.risk.dynamic_sl_tp import DynamicSLTP

    # Пример конфигурации
    config = {
        "enabled": True,
        "sl_multiplier": 0.02,
        "tp_multiplier": 0.04
    }

    # Пример входных данных
    df = pd.DataFrame({
        "timestamp": ["2024-01-01 00:00:00"],
        "symbol": ["BTCUSDT"],
        "entry_price": [100.0],
        "side": ["long"]
    })

    sltp = DynamicSLTP(config)
    result = sltp.apply(df.copy())

    assert "sl" in result.columns
    assert "tp" in result.columns
    assert result.iloc[0]["sl"] == pytest.approx(98.0)
    assert result.iloc[0]["tp"] == pytest.approx(104.0)
