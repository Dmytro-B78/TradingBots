# ============================================
# File: tests/test_riskguard_block_cooldown.py
# Purpose: Test cooldown blocking logic in RiskGuard
# Format: UTF-8 without BOM
# ASCII only (no Cyrillic)
# ============================================

import csv
from bot_ai.risk.guard import RiskGuard


class DummyCtx:
    def __init__(self, symbol="BTCUSDT", vol24h_usdt=5000, spread_pct=0,
                 daily_pnl_usdt=0, equity_usdt=1000, price=100, mode="paper"):
        self.symbol = symbol
        self.vol24h_usdt = vol24h_usdt
        self.spread_pct = spread_pct
        self.daily_pnl_usdt = daily_pnl_usdt
        self.equity_usdt = equity_usdt
        self.price = price
        self.mode = mode


def test_cooldown_block(tmp_path, monkeypatch):
    # Ensure logs directory exists inside tmp_path
    logs_dir = tmp_path / "logs"
    logs_dir.mkdir()

    # Force RiskGuard to write logs into tmp_path/logs
    monkeypatch.chdir(tmp_path)

    guard = RiskGuard(cfg={"risk": {"cooldown_minutes": 5}})
    ctx = DummyCtx()

    # First call must pass
    result1 = guard.check(ctx)
    assert result1 is True

    # Second call must be blocked
    result2 = guard.check(ctx)
    assert result2 is False

    # Log file must exist
    risk_blocks = logs_dir / "risk_blocks.csv"
    assert risk_blocks.exists()

    # Log must contain at least one row
    with risk_blocks.open("r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) > 0

    last = rows[-1]

    # Validate fields
    assert last["symbol"] == "BTCUSDT"
    assert last["reason"] == "cooldown"

    # Details must contain the word "cooldown"
    assert "cooldown" in last["details"]

    assert last["mode"] == "paper"
