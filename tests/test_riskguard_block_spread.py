from bot_ai.risk.risk_guard import RiskGuard, TradeContext

def test_spread_block():
    cfg = type("Cfg", (), {})()
    cfg.risk = type("RiskCfg", (), {
        "max_spread": 0.5
    })()

    ctx = TradeContext()
    ctx.spread = 0.8  # превышает лимит

    guard = RiskGuard(cfg)
    allowed = guard.check(ctx)

    assert allowed is False
    assert "Spread too wide" in guard.get_blocked_reasons()

def test_spread_not_blocked():
    cfg = type("Cfg", (), {})()
    cfg.risk = type("RiskCfg", (), {
        "max_spread": 0.5
    })()

    ctx = TradeContext()
    ctx.spread = 0.3  # в пределах лимита

    guard = RiskGuard(cfg)
    allowed = guard.check(ctx)

    assert allowed
    assert guard.get_blocked_reasons() == []

