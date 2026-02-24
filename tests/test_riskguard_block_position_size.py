from bot_ai.risk.risk_guard import RiskGuard, TradeContext

def test_position_size_block():
    cfg = type("Cfg", (), {})()
    cfg.risk = type("RiskCfg", (), {})()

    ctx = TradeContext()
    ctx.position_size = 0  # некорректный размер

    guard = RiskGuard(cfg)
    allowed = guard.check(ctx)

    assert allowed is False
    assert "Invalid position size" in guard.get_blocked_reasons()

def test_position_size_not_blocked():
    cfg = type("Cfg", (), {})()
    cfg.risk = type("RiskCfg", (), {})()

    ctx = TradeContext()
    ctx.position_size = 100  # допустимый размер

    guard = RiskGuard(cfg)
    allowed = guard.check(ctx)

    assert allowed
    assert guard.get_blocked_reasons() == []

