import logging

import pandas as pd

def test_dynamic_sltp_all_branches(caplog):
    from bot_ai.risk.dynamic_sl_tp import DynamicSLTP

    # Фиктивный cfg с нужными параметрами
    cfg = type("Cfg", (), {})()
    cfg.risk = type("RiskCfg", (), {
        "sl_atr_multiplier": 2.0,
        "tp_atr_multiplier": 3.0,
        "atr_period": 2
    })()
    cfg.sl_tp = type("SlTpCfg", (), {
        "sl_value": 2.0,
        "tp_value": 3.0
    })()

    sltp = DynamicSLTP(cfg)

    # 1. Нет данных OHLCV
    caplog.set_level(logging.WARNING)
    sl, tp = sltp.calculate(None, {"Price": 100, "Side": "buy"})
    assert sl is None and tp is None
    assert any("нет данных OHLCV" in m for m in caplog.messages)

    # 2. ATR <= 0
    df_zero_atr = pd.DataFrame(
        {"high": [1, 1], "low": [1, 1], "close": [1, 1]})
    sl, tp = sltp.calculate(df_zero_atr, {"Price": 100, "Side": "buy"})
    assert sl is None and tp is None

    # 3. Нет цены входа
    df = pd.DataFrame({"high": [2, 3], "low": [1, 2], "close": [1.5, 2.5]})
    sl, tp = sltp.calculate(df, {"Side": "buy"})
    assert sl is None and tp is None

    # 4. Неизвестная сторона сделки
    sl, tp = sltp.calculate(df, {"Price": 100, "Side": "hold"})
    assert sl is None and tp is None

    # 5. Покупка
    sl, tp = sltp.calculate(df, {"Price": 100, "Side": "buy"})
    assert sl < 100 and tp > 100

    # 6. Продажа
    sl, tp = sltp.calculate(df, {"Price": 100, "Side": "sell"})
    assert sl > 100 and tp < 100

