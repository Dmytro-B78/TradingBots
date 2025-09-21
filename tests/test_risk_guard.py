# tests/test_risk_guard.py
# Проверка работы RiskGuard из bot_ai/risk/risk_guard.py

import pytest
from bot_ai.risk.risk_guard import RiskGuard, TradeContext


def test_risk_guard_daily_loss_and_kill_switch():
    cfg = {"risk": {"max_daily_loss_pct": 1, "kill_switch_loss_pct": 5}}
    rg = RiskGuard(cfg)

    # До убытков сделка разрешена
    ctx = TradeContext(symbol="BTCUSDT", side="BUY", price=100, equity_usdt=10_000,
                       daily_pnl_usdt=0, spread_pct=0.1, vol24h_usdt=1_000_000)
    assert rg.check(ctx) is True

    # Превышение дневного убытка (5% от equity)
    ctx = TradeContext(symbol="BTCUSDT", side="BUY", price=100, equity_usdt=10_000,
                       daily_pnl_usdt=-500, spread_pct=0.1, vol24h_usdt=1_000_000)
    assert rg.check(ctx) is False

    # Превышение общего убытка
    rg.total_loss_pct = 10
    ctx = TradeContext(symbol="BTCUSDT", side="BUY", price=100, equity_usdt=10_000,
                       daily_pnl_usdt=0, spread_pct=0.1, vol24h_usdt=1_000_000)
    assert rg.check(ctx) is False
