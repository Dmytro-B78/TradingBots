import pytest

def test_executor_trade(tmp_path):
    """
    Тестирует выброс ValueError при попытке записать неполную сделку.
    """
    from bot_ai.exec.executor import TradeExecutor

    # Создаём экземпляр TradeExecutor
    te = TradeExecutor(log_file=tmp_path / "trades.csv", mode="paper", risk_guard=None)

    # Сделка без обязательного поля qty
    trade = {
        "symbol": "BTCUSDT",
        "side": "BUY",
        "price": 100.0
    }

    # Ожидаем ValueError
    with pytest.raises(ValueError):
        te.log_trade_to_csv(trade)
