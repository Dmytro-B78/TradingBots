import csv
import uuid
from pathlib import Path

from bot_ai.exec.executor import TradeExecutor

def test_executor_logging_basic(tmp_path):
    log_file = tmp_path / "trades_log.csv"
    executor = TradeExecutor(log_file=str(log_file), mode="paper")

    trade = {
        "symbol": "BTCUSDT",
        "side": "BUY",
        "price": 27000.5,
        "qty": 0.01,
        "sl": 26500.0,
        "tp": 28000.0
    }

    assert Path(log_file).exists()

    with open(log_file, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 1
    logged = rows[0]

    # Проверка UUID
    uuid_obj = uuid.UUID(logged["trade_id"])
    assert str(uuid_obj) == logged["trade_id"]

    # Проверка режима и источника
    assert logged["mode"] == "paper"
    assert logged["signal_source"] == "unit_test"

    # Проверка обязательных полей
    assert logged["symbol"] == "BTCUSDT"
    assert logged["side"] == "BUY"
    assert float(logged["price"]) == 27000.5
    assert float(logged["qty"]) == 0.01

