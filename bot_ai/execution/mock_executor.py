# -*- coding: utf-8 -*-
# ============================================
# 📂 File: bot_ai/execution/mock_executor.py
# ⚙️ Назначение: Эмуляция исполнения сделок
# ============================================

import logging

class MockExecutor:
    def __init__(self):
        self.position = None
        self.trades = []

    def execute(self, signal, price, timestamp):
        log = logging.getLogger("executor")

        if self.position:
            holding_period = timestamp - self.position["entry_time"]
            pnl = (price - self.position["entry_price"]) * self.position["side"]
            log.info(f"[EXEC] Закрытие позиции: {'SELL' if self.position['side'] == 1 else 'BUY'} @ {price:.2f} | PnL: {pnl:.2f} | Держали: {holding_period} тиков")
            self.trades.append({
                "entry_time": self.position["entry_time"],
                "exit_time": timestamp,
                "side": self.position["side"],
                "entry_price": self.position["entry_price"],
                "exit_price": price,
                "pnl": pnl,
                "holding_period": holding_period
            })
            self.position = None

        if signal in [1, -1]:
            self.position = {
                "side": signal,
                "entry_price": price,
                "entry_time": timestamp
            }
            log.info(f"[EXEC] Открытие позиции: {'BUY' if signal == 1 else 'SELL'} @ {price:.2f}")
