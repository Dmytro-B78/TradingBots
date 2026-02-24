# ============================================
# Path: C:\TradingBots\NT\bot_ai\execution\mock_executor.py
# Purpose: Mock executor for simulating trade entries and exits
# Used in backtesting strategies
# Format: UTF-8 without BOM, production-ready
# ============================================

import logging

class MockExecutor:
    def __init__(self):
        self.position = None
        self.trades = []

    def execute(self, signal, price, timestamp):
        log = logging.getLogger("executor")

        # Close existing position
        if self.position:
            holding_period = timestamp - self.position["entry_time"]
            pnl = (price - self.position["entry_price"]) * self.position["side"]
            log.info(f"[EXEC] CLOSE {'SELL' if self.position['side'] == 1 else 'BUY'} @ {price:.2f} | PnL: {pnl:.2f} | Duration: {holding_period}")
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

        # Open new position
        if signal in [1, -1]:
            self.position = {
                "side": signal,
                "entry_price": price,
                "entry_time": timestamp
            }
            log.info(f"[EXEC] OPEN {'BUY' if signal == 1 else 'SELL'} @ {price:.2f}")
