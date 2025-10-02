import csv
from pathlib import Path
from bot_ai.risk.risk_guard import RiskGuardWithLogging, TradeContext

def test_kill_switch_block(tmp_path, monkeypatch):
    logs_dir = tmp_path / "logs"
    logs_dir.mkdir()
    monkeypatch.chdir(tmp_path)

    guard = RiskGuardWithLogging(config={"risk": {}})
    guard.kill_switch_triggered = True

    ctx = TradeContext(
        symbol="DOGEUSDT", side="sell", price=0.1,
        equity_usdt=1000, daily_pnl_usdt=0,
        spread_pct=0, vol24h_usdt=5000
    )

    allowed = guard.check(ctx)
    assert allowed is False

    risk_blocks = logs_dir / "risk_blocks.csv"
    assert risk_blocks.exists()
