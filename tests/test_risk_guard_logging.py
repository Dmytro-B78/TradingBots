# tests/test_risk_guard_logging.py
# Проверка логирования отказов и успешных сделок RiskGuard

import csv
from bot_ai.risk.risk_guard import RiskGuard, TradeContext


def make_ctx(**kwargs):
    defaults = dict(
        symbol="BTCUSDT",
        side="BUY",
        price=100,
        equity_usdt=10_000,
        daily_pnl_usdt=0,
        spread_pct=0.1,
        vol24h_usdt=1_000_000,
    )
    defaults.update(kwargs)
    return TradeContext(**defaults)


def test_risk_guard_logs_denials_and_passes(tmp_path):
    deny_file = tmp_path / "risk_log.csv"
    pass_file = tmp_path / "risk_pass_log.csv"

    # Конфиг: max_positions=0 → всегда отказ
    cfg = {"risk": {"max_positions": 0}}
    rg = RiskGuard(cfg, risk_log_file=deny_file, risk_pass_log_file=pass_file)

    ctx = make_ctx()
    allowed = rg.check(ctx)
    assert allowed is False

    # Проверяем, что отказ записан
    rows = list(csv.reader(deny_file.open(encoding="utf-8")))
    assert rows[0] == ["timestamp", "message"]
    assert "Открытых позиций" in rows[1][1]

    # Теперь разрешим сделки
    cfg = {"risk": {"max_positions": 10}}
    rg = RiskGuard(cfg, risk_log_file=deny_file, risk_pass_log_file=pass_file)

    ctx = make_ctx()
    allowed = rg.check(ctx)
    assert allowed is True

    # Проверяем, что успешная сделка записана
    rows = list(csv.reader(pass_file.open(encoding="utf-8")))
    assert rows[0] == ["timestamp", "message"]
    assert "Сделка разрешена" in rows[1][1]
