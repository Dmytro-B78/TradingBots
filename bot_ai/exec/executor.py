# bot_ai/exec/executor.py
# Полная версия файла. Добавлено:
# - Уникальный идентификатор сделки (trade_id, UUID4)
# - Режим работы (mode: "paper" или "live")
# - Источник сигнала (signal_source)
# - Мини-тест в блоке __main__
# - Исправлено предупреждение: datetime.now(timezone.utc)

import csv
import os
import uuid
from datetime import datetime, timezone
from typing import Dict, Any, Optional


class TradeExecutor:
    """
    Исполнитель сделок: логирование в CSV с уникальным ID, режимом и источником сигнала.
    """

    def __init__(self, log_file: str = "trades_log.csv", mode: str = "paper") -> None:
        """
        Параметры:
        - log_file: путь к CSV-файлу логирования сделок.
        - mode: режим работы бота, допустимые значения: "paper" или "live".
        """
        self.log_file = log_file
        self.mode = self._validate_mode(mode)

    @staticmethod
    def _validate_mode(mode: str) -> str:
        """
        Валидация режима работы. Возвращает корректное значение или поднимает ValueError.
        """
        allowed = {"paper", "live"}
        normalized = str(mode).strip().lower()
        if normalized not in allowed:
            raise ValueError(f"Invalid mode '{mode}'. Allowed: {sorted(allowed)}")
        return normalized

    def log_trade_to_csv(self, trade: Dict[str, Any], signal_source: str = "unknown") -> str:
        """
        Логирование сделки в CSV.

        Обязательные ключи trade:
        - symbol: строка, тикер инструмента (пример: "BTCUSDT")
        - side: строка, "BUY" или "SELL"
        - price: число, цена исполнения
        - qty: число, количество
        Необязательные ключи:
        - sl: число, стоп-лосс
        - tp: число, тейк-профит

        Возвращает:
        - trade_id (строка UUID), под которым сделка записана.
        """
        self._validate_trade(trade)

        file_exists = os.path.isfile(self.log_file)
        trade_id = str(uuid.uuid4())

        row = {
            "trade_id": trade_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "symbol": trade.get("symbol"),
            "side": trade.get("side"),
            "price": self._to_number(trade.get("price")),
            "qty": self._to_number(trade.get("qty")),
            "sl": self._to_number(trade.get("sl")),
            "tp": self._to_number(trade.get("tp")),
            "mode": self.mode,
            "signal_source": str(signal_source),
        }

        fieldnames = [
            "trade_id", "timestamp", "symbol", "side",
            "price", "qty", "sl", "tp", "mode", "signal_source"
        ]

        directory = os.path.dirname(self.log_file)
        if directory and not os.path.isdir(directory):
            os.makedirs(directory, exist_ok=True)

        with open(self.log_file, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()
            writer.writerow(row)

        return trade_id

    @staticmethod
    def _to_number(value: Optional[Any]) -> Optional[float]:
        if value is None or value == "":
            return None
        try:
            return float(value)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"Value '{value}' must be a number or None") from exc

    @staticmethod
    def _validate_trade(trade: Dict[str, Any]) -> None:
        required = ["symbol", "side", "price", "qty"]
        for key in required:
            if key not in trade:
                raise ValueError(f"Missing required trade field: '{key}'")

        symbol = str(trade.get("symbol")).strip()
        side = str(trade.get("side")).strip().upper()

        if not symbol:
            raise ValueError("Field 'symbol' must be non-empty string")

        if side not in {"BUY", "SELL"}:
            raise ValueError("Field 'side' must be 'BUY' or 'SELL'")

        for k in ["price", "qty"]:
            if trade.get(k) is None:
                raise ValueError(f"Field '{k}' must not be None")
            _ = TradeExecutor._to_number(trade.get(k))
        if trade.get("sl") is not None:
            _ = TradeExecutor._to_number(trade.get("sl"))
        if trade.get("tp") is not None:
            _ = TradeExecutor._to_number(trade.get("tp"))


if __name__ == "__main__":
    executor = TradeExecutor(log_file="trades_log.csv", mode="paper")
    trade = {
        "symbol": "BTCUSDT",
        "side": "BUY",
        "price": 27000.5,
        "qty": 0.01,
        "sl": 26500.0,
        "tp": 28000.0
    }
    trade_id = executor.log_trade_to_csv(trade, signal_source="AI_strategy")
    print(f"✅ Сделка записана в trades_log.csv, trade_id={trade_id}")
