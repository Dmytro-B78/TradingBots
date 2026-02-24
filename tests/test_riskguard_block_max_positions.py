from bot_ai.risk.risk_guard import RiskGuard, TradeContext

def test_max_positions_block():
    cfg = type("Cfg", (), {})()
    cfg.risk = type("RiskCfg", (), {
        "max_positions": 5
    })()

    ctx = TradeContext()
    ctx.max_positions = 5  # достигнут лимит

    guard = RiskGuard(cfg)
    allowed = guard.check(ctx)

    assert allowed is False
    assert "Max positions reached" in guard.get_blocked_reasons()

def test_max_positions_not_blocked():
    cfg = type("Cfg", (), {})()
    cfg.risk = type("RiskCfg", (), {
        "max_positions": 5
    })()

    ctx = TradeContext()
    ctx.max_positions = 3  # ниже лимита

    guard = RiskGuard(cfg)
    allowed = guard.check(ctx)

    assert allowed
    assert guard.get_blocked_reasons() == []

