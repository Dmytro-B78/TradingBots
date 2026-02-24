import pytest
from bot_ai.execution.executor import TradeExecutor

def test_executor_trade(tmp_path):
    """
    Проверяет, что log_trade_to_csv выбрасывает ValueError,
    если в трейде отсутствует обязательное поле qty.
    """
    log_file = tmp_path / "trades.csv"
    te = TradeExecutor(log_file=log_file, mode="paper", risk_guard=None)

    # Трейд без qty → должен вызвать ValueError
    trade = {
        "symbol": "BTCUSDT",
        "side": "BUY",
        "price": 100.0
    }

    with pytest.raises(ValueError, match="qty"):
        te.log_trade_to_csv(trade)
