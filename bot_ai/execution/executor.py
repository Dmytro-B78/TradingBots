"""
Исполнитель торговых решений: открытие и закрытие сделок, логирование, отправка уведомлений.
"""

from datetime import datetime, timezone
import csv

class TradeExecutor:
    def __init__(self, log_file=None, mode="live", notifier=None, risk_guard=None):
        if mode not in ("live", "paper"):
            raise ValueError(f"Недопустимый режим: {mode}")
        self.log_file = log_file
        self.mode = mode
        self.notifier = notifier
        self.risk_guard = risk_guard

    def open_trade(self, symbol, side, price, size, sl, tp):
        trade = {
            "symbol": symbol,
            "side": side,
            "price": price,
            "size": size,
            "sl": sl,
            "tp": tp,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self.risk_guard and not self.risk_guard.check(trade):
            return None

        if self.notifier:
            self.notifier.trade_open(trade)

        if self.mode == "paper" and self.log_file:
            self._log_trade(trade, action="open")

        return trade

    def close_trade(self, trade):
        trade["closed_at"] = datetime.now(timezone.utc).isoformat()

        if self.notifier:
            self.notifier.trade_close(trade)

        if self.mode == "paper" and self.log_file:
            self._log_trade(trade, action="close")

        return trade

    def _log_trade(self, trade, action):
        row = trade.copy()
        row["action"] = action
        fieldnames = list(row.keys())

        with open(self.log_file, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            if f.tell() == 0:
                writer.writeheader()
            writer.writerow(row)

    def log_trade_to_csv(self, trade: dict, signal_source: str = "unknown"):
        if "qty" not in trade:
            raise ValueError("Поле 'qty' обязательно для логирования трейда")

        if self.risk_guard and not self.risk_guard.check(trade):
            raise PermissionError("RiskGuard запретил логирование трейда")

        row = trade.copy()
        row["signal_source"] = signal_source
        row["timestamp"] = datetime.now(timezone.utc).isoformat()
        fieldnames = list(row.keys())

        if not self.log_file:
            raise ValueError("log_file не задан")

        with open(self.log_file, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            if f.tell() == 0:
                writer.writeheader()
            writer.writerow(row)

        return row

    @staticmethod
    def _to_number(value):
        try:
            return float(value)
        except (ValueError, TypeError):
            return None
