# -*- coding: utf-8 -*-
# ============================================
# File: tests/test_sl_tp.py
# Назначение: Юнит?тесты для стратегии SLTPStrategy
# Обновления:
# - Проверка структуры сигнала
# - Проверка расчёта SL и TP
# ============================================

import unittest

import pandas as pd

from strategies.sl_tp import SLTPStrategy

class TestSLTPStrategy(unittest.TestCase):
    def setUp(self):
        self.cfg = {
            "sl_pct": 0.01,
            "tp_pct": 0.02
        }
        self.strategy = SLTPStrategy(self.cfg)
        dates = pd.date_range(end=pd.Timestamp.today(), periods=3)
        prices = [100, 101, 102]
        self.df = pd.DataFrame({
            "date": dates,
            "open": [99, 100, 101],
            "high": [101, 102, 103],
            "low": [98, 99, 100],
            "close": prices,
            "volume": [1000, 1100, 1200]
        }).set_index("date")

    def test_run_returns_trade(self):
        trades = self.strategy.run("BTC/USDT", self.df.copy())
        self.assertEqual(len(trades), 1)
        trade = trades[0]
        self.assertIn("pair", trade)
        self.assertIn("signal", trade)
        self.assertIn("entry_price", trade)
        self.assertIn("sl", trade)
        self.assertIn("tp", trade)

    def test_sl_tp_calculation(self):
        trades = self.strategy.run("BTC/USDT", self.df.copy())
        trade = trades[0]
        entry = trade["entry_price"]
        if trade["signal"] == "long":
            self.assertAlmostEqual(trade["sl"], round(
                entry * (1 - self.cfg["sl_pct"]), 2))
            self.assertAlmostEqual(trade["tp"], round(
                entry * (1 + self.cfg["tp_pct"]), 2))
        else:
            self.assertAlmostEqual(trade["sl"], round(
                entry * (1 + self.cfg["sl_pct"]), 2))
            self.assertAlmostEqual(trade["tp"], round(
                entry * (1 - self.cfg["tp_pct"]), 2))

if __name__ == "__main__":
    unittest.main()

