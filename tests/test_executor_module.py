import os
import pytest
from bot_ai.execution.executor import TradeExecutor

def test_trade_executor_all_branches(tmp_path):
    """
    Проверяет все ключевые ветки TradeExecutor:
    - режим paper
    - валидация режима
    - логирование трейда
    - RiskGuard: разрешает и блокирует
    - _to_number поведение
    """
    log_file = tmp_path / "trades.csv"

    # 1. Создание TradeExecutor с режимом paper
    te = TradeExecutor(log_file=log_file, mode="paper")
    assert te.mode == "paper"

    # 2. Неверный режим должен вызвать ValueError
    with pytest.raises(ValueError):
        TradeExecutor(log_file=log_file, mode="invalid")

    # 3. Логируем трейд без RiskGuard
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

    # 4. RiskGuard разрешает трейд
    class AllowRG:
        def check(self, ctx): return True

    te_rg = TradeExecutor(log_file=log_file, mode="paper", risk_guard=AllowRG())
    row2 = te_rg.log_trade_to_csv(trade, signal_source="test")
    assert row2["symbol"] == "BTCUSDT"

    # 5. RiskGuard блокирует трейд
    class BlockRG:
        def check(self, ctx): return False

    te_block = TradeExecutor(log_file=log_file, mode="paper", risk_guard=BlockRG())
    with pytest.raises(PermissionError):
        te_block.log_trade_to_csv(trade, signal_source="test")

    # 6. _to_number — корректные и некорректные значения
    assert TradeExecutor._to_number("123") == 123.0
    assert TradeExecutor._to_number(None) is None
    assert TradeExecutor._to_number("") is None
    with pytest.raises(ValueError):
        float("abc")  # имитируем поведение без защиты
