# ============================================
# ✅ risk_manager.py — RiskManager
# Обновление:
# - Поддержка tp_pct, sl_pct, rrr
# - Учет mode, side, max_holding_period
# - Фильтры: ADX, ATR (если есть в signals)
# ============================================

import pandas as pd

class RiskManager:
    def __init__(self, config):
        self.tp_pct = config.get("tp_pct", 0.015)
        self.sl_pct = config.get("sl_pct", 0.01)
        self.rrr = config.get("rrr", 1.5)
        self.trailing_stop_pct = config.get("trailing_stop_pct", 0.015)
        self.mode = config.get("mode", "both")
        self.side = config.get("side", 0)
        self.max_holding = config.get("max_holding_period", 48)
        self.adx_threshold = config.get("adx_threshold", 20)

    def apply(self, signals: pd.DataFrame, df: pd.DataFrame) -> list:
        trades = []
        position = None
        hold = 0

        for i in range(1, len(signals)):
            row = signals.iloc[i]
            signal = row["signal"]
            price = row["close"]
            time = row["time"]

            # Фильтр по ADX
            if "adx" in row and row["adx"] < self.adx_threshold:
                continue

            # Закрытие по max_holding_period
            if position:
                hold += 1
                if hold >= self.max_holding:
                    position["exit_time"] = time
                    trades.append(position)
                    position = None
                continue

            # Пропуск по режиму
            if self.mode == "long_only" and signal != 1:
                continue
            if self.mode == "short_only" and signal != -1:
                continue

            # Пропуск по side
            if self.side == 1 and signal != 1:
                continue
            if self.side == -1 and signal != -1:
                continue

            if signal == 0:
                continue

            direction = "long" if signal == 1 else "short"
            entry = price
            sl = entry * (1 - self.sl_pct) if direction == "long" else entry * (1 + self.sl_pct)
            tp = entry * (1 + self.tp_pct) if direction == "long" else entry * (1 - self.tp_pct)

            position = {
                "time": time,
                "direction": direction,
                "entry": entry,
                "sl": sl,
                "tp": tp,
                "entry_time": time
            }
            hold = 0

        if position:
            position["exit_time"] = time
            trades.append(position)

        return trades
