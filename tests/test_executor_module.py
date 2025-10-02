import os
import pytest

def test_trade_executor_all_branches(tmp_path):
    from bot_ai.exec.executor import TradeExecutor

    log_file = tmp_path / "trades.csv"

    # 1. Валидный режим
    te = TradeExecutor(log_file=log_file, mode="paper")
    assert te.mode == "paper"

    # 2. Невалидный режим
    with pytest.raises(ValueError):
        TradeExecutor(log_file=log_file, mode="invalid")

    # 3. Запись сделки без RiskGuard
    trade = {
        "symbol": "BTCUSDT",
        "side": "BUY",
        "price": 100.0,
        "qty": 1.0,
        "sl": 90.0,
        "tp": 110.0
    }
    row = te.log_trade_to_csv(trade, signal_source="test")
    assert row["symbol"] == "BTCUSDT"
    assert os.path.isfile(log_file)

    # 4. RiskGuard разрешает сделку
    class AllowRG:
        def check(self, ctx): return True
    te_rg = TradeExecutor(log_file=log_file, mode="paper", risk_guard=AllowRG())
    row2 = te_rg.log_trade_to_csv(trade)
    assert row2["symbol"] == "BTCUSDT"

    # 5. RiskGuard блокирует сделку
    class BlockRG:
        def check(self, ctx): return False
    te_block = TradeExecutor(log_file=log_file, mode="paper", risk_guard=BlockRG())
    with pytest.raises(PermissionError):
        te_block.log_trade_to_csv(trade)

    # 6. _to_number — корректное число
    assert TradeExecutor._to_number("123") == 123.0
    # None → None
    assert TradeExecutor._to_number(None) is None
    # Пустая строка → None
    assert TradeExecutor._to_number("") is None
    # Некорректное значение → ValueError
    with pytest.raises(ValueError):
        TradeExecutor._to_number("abc")

    # 7. _validate_trade — отсутствие обязательного поля
    bad_trade = {"symbol": "BTCUSDT", "side": "BUY", "price": 100.0}
    with pytest.raises(ValueError):
        TradeExecutor._validate_trade(bad_trade)

    # Пустой символ
    bad_trade2 = {"symbol": "", "side": "BUY", "price": 100.0, "qty": 1.0}
    with pytest.raises(ValueError):
        TradeExecutor._validate_trade(bad_trade2)

    # Неверная сторона
    bad_trade3 = {"symbol": "BTCUSDT", "side": "HOLD", "price": 100.0, "qty": 1.0}
    with pytest.raises(ValueError):
        TradeExecutor._validate_trade(bad_trade3)

    # None в цене
    bad_trade4 = {"symbol": "BTCUSDT", "side": "BUY", "price": None, "qty": 1.0}
    with pytest.raises(ValueError):
        TradeExecutor._validate_trade(bad_trade4)
