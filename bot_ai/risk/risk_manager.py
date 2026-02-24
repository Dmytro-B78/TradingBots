# -*- coding: utf-8 -*-
# ============================================
# File: bot_ai/risk/risk_manager.py
# Назначение: Управление рисками и симуляция сделок по сигналам
# Класс: RiskManager — рассчитывает SL/TP, проверяет RRR, логирует сделки
# ============================================

import os
import csv
import pandas as pd

class RiskManager:
    def __init__(self, config):
        self.pair = config.get("pair", "BTCUSDT")
        self.qty = config.get("qty", 0.01)
        self.strategy = config.get("strategy", "unknown")
        self.interval = config.get("interval", "1h")
        self.capital = config.get("capital", 10000)
        self.risk_per_trade = config.get("risk_per_trade", 0.01)
        self.min_rrr = config.get("min_risk_reward_ratio", 1.5)
        self.stop_loss_pct = config.get("stop_loss_pct", 0.02)
        self.max_holding_period = config.get("max_holding_period", 48)
        self.log_path = os.path.join("state", "trades_log.csv")
        os.makedirs("state", exist_ok=True)

    def apply(self, signals, df):
        print(f"[RiskManager] apply() — входящих сигналов: {len(signals)}")
        trades = []

        for signal in signals:
            try:
                time = signal.get("time")
                direction = signal.get("direction")
                entry = signal.get("entry")

                if time is None or direction not in ("long", "short") or entry is None:
                    print(f"[RiskManager] Пропущен сигнал с некорректными данными: {signal}")
                    continue

                entry_idx = df.index[df["time"] == time]
                if entry_idx.empty:
                    print(f"[RiskManager] Не найден индекс входа в df по времени: {time}")
                    continue

                idx = entry_idx[0]
                future = df.iloc[idx+1 : idx+1+self.max_holding_period]
                if future.empty:
                    print(f"[RiskManager] Недостаточно данных для оценки сделки: {time}")
                    continue

                sl = entry * (1 - self.stop_loss_pct) if direction == "long" else entry * (1 + self.stop_loss_pct)
                tp = entry + (entry - sl) * self.min_rrr if direction == "long" else entry - (sl - entry) * self.min_rrr
                rrr = abs((tp - entry) / (entry - sl)) if (entry - sl) != 0 else 0

                if rrr < self.min_rrr:
                    print(f"[RiskManager] Пропущен сигнал из-за низкого RRR ({rrr:.2f}): {signal}")
                    continue

                risk_amount = self.capital * self.risk_per_trade
                stop_size = abs(entry - sl)
                position_size = risk_amount / stop_size if stop_size > 0 else 0

                if position_size <= 0:
                    print(f"[RiskManager] Пропущен сигнал из-за нулевого размера позиции: {signal}")
                    continue

                exit_price = None
                exit_reason = "timeout"

                for _, row in future.iterrows():
                    high = row["high"]
                    low = row["low"]

                    if direction == "long":
                        if low <= sl:
                            exit_price = sl
                            exit_reason = "sl_hit"
                            break
                        if high >= tp:
                            exit_price = tp
                            exit_reason = "tp_hit"
                            break
                    else:
                        if high >= sl:
                            exit_price = sl
                            exit_reason = "sl_hit"
                            break
                        if low <= tp:
                            exit_price = tp
                            exit_reason = "tp_hit"
                            break

                if exit_price is None:
                    exit_price = future.iloc[-1]["close"]

                pnl = (exit_price - entry) * position_size if direction == "long" else (entry - exit_price) * position_size

                trade = {
                    "time": time,
                    "pair": self.pair,
                    "strategy": self.strategy,
                    "interval": self.interval,
                    "direction": direction,
                    "entry": round(entry, 4),
                    "sl": round(sl, 4),
                    "tp": round(tp, 4),
                    "exit": round(exit_price, 4),
                    "exit_reason": exit_reason,
                    "rrr": round(rrr, 2),
                    "qty": round(position_size, 4),
                    "pnl": round(pnl, 2)
                }

                trades.append(trade)
                self._log_trade(trade)

            except Exception as e:
                print(f"[RiskManager] Ошибка при обработке сигнала {signal}: {e}")

        print(f"[RiskManager] Обработано сделок: {len(trades)}")
        return trades

    def _log_trade(self, trade):
        file_exists = os.path.isfile(self.log_path)
        with open(self.log_path, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=trade.keys())
            if not file_exists:
                writer.writeheader()
            writer.writerow(trade)
