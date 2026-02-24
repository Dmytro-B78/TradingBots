from bot_ai.risk.risk_guard import RiskGuard, TradeContext

def test_risk_per_trade_block():
    cfg = type("Cfg", (), {})()
    cfg.risk = type("RiskCfg", (), {
        "max_risk_per_trade": 0.02
    })()

    ctx = TradeContext()
    ctx.risk_per_trade = 0.05  # превышает лимит

    guard = RiskGuard(cfg)
    allowed = guard.check(ctx)

    assert allowed is False
    assert "Risk per trade too high" in guard.get_blocked_reasons()

def test_risk_per_trade_not_blocked():
    cfg = type("Cfg", (), {})()
    cfg.risk = type("RiskCfg", (), {
        "max_risk_per_trade": 0.02
    })()

    ctx = TradeContext()
    ctx.risk_per_trade = 0.01  # в пределах лимита

    guard = RiskGuard(cfg)
    allowed = guard.check(ctx)

    assert allowed
    assert guard.get_blocked_reasons() == []

