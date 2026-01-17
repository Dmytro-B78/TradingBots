import csv
import uuid
<<<<<<< HEAD
from pathlib import Path
=======
<<<<<<< Updated upstream
from typing import List, Dict
=======
from pathlib import Path
>>>>>>> Stashed changes
>>>>>>> 47a38855 (🔥 Финальный merge: stage0.4_main_release → main, конфликты решены)

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
<<<<<<< HEAD
=======
<<<<<<< Updated upstream
    trade2 = {
        "symbol": "ETHUSDT",
        "side": "SELL",
        "price": 1700.0,
        "qty": 0.5,
        "sl": 1750.0,
        "tp": 1600.0
    }
=======
>>>>>>> Stashed changes
>>>>>>> 47a38855 (🔥 Финальный merge: stage0.4_main_release → main, конфликты решены)

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

<<<<<<< HEAD
=======
<<<<<<< Updated upstream
    # Повторная запись не должна дублировать заголовок
    id3 = executor.log_trade_to_csv(trade1, signal_source="manual")
    rows2 = read_csv(str(log_path))
    assert len(rows2) == 3
    assert rows2[-1]["signal_source"] == "manual"
=======
    # Проверка обязательных полей
    assert logged["symbol"] == "BTCUSDT"
    assert logged["side"] == "BUY"
    assert float(logged["price"]) == 27000.5
    assert float(logged["qty"]) == 0.01

>>>>>>> Stashed changes
>>>>>>> 47a38855 (🔥 Финальный merge: stage0.4_main_release → main, конфликты решены)
