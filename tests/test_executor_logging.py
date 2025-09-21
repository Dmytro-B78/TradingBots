#  python -m pytest -v tests\test_executor_logging.py
# tests/test_executor_logging.py
# Проверка логирования сделок в executor.py

import os
import csv
import uuid
from typing import List, Dict

from bot_ai.exec.executor import TradeExecutor


def read_csv(path: str) -> List[Dict[str, str]]:
    if not os.path.isfile(path):
        return []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def test_executor_logging_basic(tmp_path):
    log_path = tmp_path / "trades_log.csv"
    executor = TradeExecutor(log_file=str(log_path), mode="paper")

    trade1 = {
        "symbol": "BTCUSDT",
        "side": "BUY",
        "price": 27000.5,
        "qty": 0.01,
        "sl": 26500.0,
        "tp": 28000.0
    }
    trade2 = {
        "symbol": "ETHUSDT",
        "side": "SELL",
        "price": 1700.0,
        "qty": 0.5,
        "sl": 1750.0,
        "tp": 1600.0
    }

    id1 = executor.log_trade_to_csv(trade1, signal_source="AI_strategy")
    id2 = executor.log_trade_to_csv(trade2, signal_source="RSI_EMA")

    # Проверка уникальности ID
    assert id1 != id2
    assert uuid.UUID(id1) and uuid.UUID(id2)

    rows = read_csv(str(log_path))
    assert len(rows) == 2

    # Проверка полей
    for row in rows:
        assert set(row.keys()) == {
            "trade_id", "timestamp", "symbol", "side",
            "price", "qty", "sl", "tp", "mode", "signal_source"
        }
        assert row["trade_id"]
        assert row["timestamp"]
        assert row["mode"] == "paper"
        assert row["symbol"] in {"BTCUSDT", "ETHUSDT"}
        assert row["side"] in {"BUY", "SELL"}
        assert row["signal_source"] in {"AI_strategy", "RSI_EMA"}

    # Повторная запись не должна дублировать заголовок
    id3 = executor.log_trade_to_csv(trade1, signal_source="manual")
    rows2 = read_csv(str(log_path))
    assert len(rows2) == 3
    assert rows2[-1]["signal_source"] == "manual"
