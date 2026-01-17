import csv

from bot_ai.risk.risk_guard import RiskGuardWithLogging, TradeContext

def test_daily_loss_block(tmp_path, monkeypatch):
    logs_dir = tmp_path / "logs"
    logs_dir.mkdir()
    monkeypatch.chdir(tmp_path)

    guard = RiskGuardWithLogging(config={"risk": {"max_daily_loss_pct": 10}})
    ctx = TradeContext(
        symbol="ETHUSDT", side="buy", price=100,
        equity_usdt=1000, daily_pnl_usdt=-200,
        spread_pct=0, vol24h_usdt=5000
    )

    allowed = guard.check(ctx)
    assert allowed is False

    risk_blocks = logs_dir / "risk_blocks.csv"
    assert risk_blocks.exists()

    with risk_blocks.open("r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    last = rows[-1]
    assert last["symbol"] == "ETHUSDT"
    assert last["reason"] == "daily_loss"

