import pytest
from bot_ai.risk.risk_guard import RiskGuard, TradeContext

def test_block_daily_loss_triggered():
    cfg = type("Cfg", (), {})()
    cfg.risk = type("RiskCfg", (), {
        "max_daily_loss": 100,
        "max_daily_loss_enabled": True
    })()
    context = TradeContext()
    context.daily_loss = 150

    guard = RiskGuard(cfg)
    allowed = guard.check(context)

    assert not allowed
    assert "Max daily loss exceeded" in guard.get_blocked_reasons()

def test_block_daily_loss_not_triggered():
    cfg = type("Cfg", (), {})()
    cfg.risk = type("RiskCfg", (), {
        "max_daily_loss": 100,
        "max_daily_loss_enabled": True
    })()
    context = TradeContext()
    context.daily_loss = 50

    guard = RiskGuard(cfg)
    allowed = guard.check(context)

    assert allowed
    assert guard.get_blocked_reasons() == []

