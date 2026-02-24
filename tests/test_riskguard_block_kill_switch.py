from bot_ai.risk.risk_guard import RiskGuard, TradeContext

def test_kill_switch_block(tmp_path, monkeypatch):
    logs_dir = tmp_path / "logs"
    logs_dir.mkdir()
    monkeypatch.chdir(tmp_path)

    cfg = type("Cfg", (), {})()
    cfg.risk = type("RiskCfg", (), {})()

    ctx = TradeContext()
    ctx.kill_switch = True

    guard = RiskGuard(cfg)
    allowed = guard.check(ctx)

    assert allowed is False
    assert "Kill switch activated" in guard.get_blocked_reasons()

