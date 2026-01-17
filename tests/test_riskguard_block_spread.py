
from bot_ai.risk.risk_guard import RiskGuardWithLogging, TradeContext

def test_spread_block(tmp_path, monkeypatch):
    logs_dir = tmp_path / "logs"
    logs_dir.mkdir()
    monkeypatch.chdir(tmp_path)

    guard = RiskGuardWithLogging(config={"risk": {"max_spread_pct": 0.5}})
    ctx = TradeContext(
        symbol="AVAXUSDT", side="sell", price=10,
        equity_usdt=1000, daily_pnl_usdt=0,
        spread_pct=1.0, vol24h_usdt=5000
    )

    allowed = guard.check(ctx)
    assert allowed is False

    risk_blocks = logs_dir / "risk_blocks.csv"
    assert risk_blocks.exists()

