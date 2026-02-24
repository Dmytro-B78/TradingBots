from bot_ai.risk.risk_guard import RiskGuard, TradeContext

def test_total_loss_block():
    cfg = type("Cfg", (), {})()
    cfg.risk = type("RiskCfg", (), {
        "max_total_loss": 500,
        "max_total_loss_enabled": True
    })()

    ctx = TradeContext()
    ctx.total_loss = 600  # превышает лимит

    guard = RiskGuard(cfg)
    allowed = guard.check(ctx)

    assert allowed is False
    assert "Max total loss exceeded" in guard.get_blocked_reasons()

def test_total_loss_not_blocked():
    cfg = type("Cfg", (), {})()
    cfg.risk = type("RiskCfg", (), {
        "max_total_loss": 500,
        "max_total_loss_enabled": True
    })()

    ctx = TradeContext()
    ctx.total_loss = 300  # в пределах лимита

    guard = RiskGuard(cfg)
    allowed = guard.check(ctx)

    assert allowed
    assert guard.get_blocked_reasons() == []

