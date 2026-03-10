# ============================================
# File: C:\TradingBots\NT\bot_ai\risk\manager.py
# Purpose: RiskManager — trailing stop + logging + fixed log path
# Encoding: UTF-8
# ============================================

import pandas as pd
import logging
import os
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)
print("[risk_manager.py] Module loaded: RiskManager ready")

class RiskManager:
    def __init__(self, config):
        self.pair = config.get("pair", "BTCUSDT")
        self.qty = config.get("qty", 0.01)
        self.strategy = config.get("strategy", "unknown")
        self.interval = config.get("interval", "1h")
        self.trailing_stop_pct = config.get("trailing_stop_pct", 0.02)
        self.take_profit_pct = config.get("take_profit_pct", 0.04)
        self.position = None

        default_path = "C:/TradingBots/NT/trades_log.csv"
        self.log_path = Path(config.get("log_path", default_path))
        print(f"[RiskManager] Logging trades to: {self.log_path.resolve()}")

    def execute(self, signal):
        price = signal.price
        side = signal.side

        if self.position is None:
            self._enter_position(signal)
            return

        entry = self.position["entry_price"]
        logger.info(f"📊 Current position: {self.position}")

        if side == "buy":
            self.position["highest_price"] = max(self.position["highest_price"], price)
            peak = self.position["highest_price"]
            stop = peak * (1 - self.trailing_stop_pct)
            tp = entry * (1 + self.take_profit_pct)

            if price <= stop:
                logger.info(f"🔻 Trailing stop hit: {price:.2f} <= {stop:.2f} — EXIT BUY")
                self._log_trade("buy", entry, price)
                self.position = None
            elif price >= tp:
                logger.info(f"🎯 Take-profit hit: {price:.2f} >= {tp:.2f} — EXIT BUY")
                self._log_trade("buy", entry, price)
                self.position = None

        elif side == "sell":
            self.position["lowest_price"] = min(self.position["lowest_price"], price)
            trough = self.position["lowest_price"]
            stop = trough * (1 + self.trailing_stop_pct)
            tp = entry * (1 - self.take_profit_pct)

            if price >= stop:
                logger.info(f"🔺 Trailing stop hit: {price:.2f} >= {stop:.2f} — EXIT SELL")
                self._log_trade("sell", entry, price)
                self.position = None
            elif price <= tp:
                logger.info(f"🎯 Take-profit hit: {price:.2f} <= {tp:.2f} — EXIT SELL")
                self._log_trade("sell", entry, price)
                self.position = None

    def _enter_position(self, signal):
        self.position = {
            "side": signal.side,
            "entry_price": signal.price,
            "highest_price": signal.price,
            "lowest_price": signal.price,
            "timestamp": datetime.utcnow().isoformat()
        }
        logger.info(f"📈 Entered {signal.side.upper()} at {signal.price:.2f}")

    def _log_trade(self, side, entry, exit_price):
        pnl = exit_price - entry if side == "buy" else entry - exit_price
        row = {
            "timestamp": datetime.utcnow().isoformat(),
            "pair": self.pair,
            "strategy": self.strategy,
            "side": side,
            "entry": round(entry, 2),
            "exit": round(exit_price, 2),
            "pnl": round(pnl, 2)
        }

        df = pd.DataFrame([row])
        header = not self.log_path.exists()
        df.to_csv(self.log_path, mode="a", header=header, index=False)
        logger.info(f"💾 Trade logged: {row}")
