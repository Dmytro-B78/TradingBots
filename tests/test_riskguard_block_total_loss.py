import csv
from pathlib import Path
from bot_ai.risk.risk_guard import RiskGuardWithLogging, TradeContext

def test_total_loss_block(tmp_path, monkeypatch):
    logs_dir = tmp_path / "logs"
    logs_dir.mkdir()
    monkeypatch.chdir(tmp_path)

    guard = RiskGuardWithLogging(config={"risk": {"kill_switch_loss_pct": 5}})
    guard.total_loss_pct = 10

    ctx = TradeContext(
        symbol="XRPUSDT", side="buy", price=100,
        equity_usdt=1000, daily_pnl_usdt=0,
        spread_pct=0, vol24h_usdt=5000
    )

    allowed = guard.check(ctx)
    assert allowed is False
    assert guard.kill_switch_triggered is True

    risk_blocks = logs_dir / "risk_blocks.csv"
    assert risk_blocks.exists()
