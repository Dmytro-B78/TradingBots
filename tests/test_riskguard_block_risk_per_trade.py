import csv
from pathlib import Path
from bot_ai.risk.risk_guard import RiskGuardWithLogging, TradeContext

def test_risk_per_trade_logging(tmp_path, monkeypatch):
    logs_dir = tmp_path / "logs"
    logs_dir.mkdir()
    monkeypatch.chdir(tmp_path)

    guard = RiskGuardWithLogging(config={"risk": {"risk_per_trade_pct": 5}})
    ctx = TradeContext(
        symbol="MATICUSDT", side="buy", price=50,
        equity_usdt=1000, daily_pnl_usdt=0,
        spread_pct=1, vol24h_usdt=10000
    )

    allowed = guard.check(ctx)
    assert allowed is True

    risk_log = Path("risk_log.csv")
    assert risk_log.exists()
