from bot_ai.risk.risk_guard import RiskGuard, TradeContext

def test_low_volume_block():
    cfg = type("Cfg", (), {})()
    cfg.risk = type("RiskCfg", (), {
        "min_24h_volume_usdt": 10000
    })()

    ctx = TradeContext()
    ctx.volume = 5000  # ниже порога

    guard = RiskGuard(cfg)
    allowed = guard.check(ctx)

    assert allowed is False
    assert "Low 24h volume" in guard.get_blocked_reasons()

def test_low_volume_not_blocked():
    cfg = type("Cfg", (), {})()
    cfg.risk = type("RiskCfg", (), {
        "min_24h_volume_usdt": 10000
    })()

    ctx = TradeContext()
    ctx.volume = 15000  # выше порога

    guard = RiskGuard(cfg)
    allowed = guard.check(ctx)

    assert allowed
    assert guard.get_blocked_reasons() == []

