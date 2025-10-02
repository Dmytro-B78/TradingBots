import csv
import time
from pathlib import Path
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
    # Подготовка временной директории logs
    logs_dir = tmp_path / "logs"
    logs_dir.mkdir()
    monkeypatch.chdir(tmp_path)  # чтобы RiskGuard писал в tmp_path/logs

    # Конфиг с кулдауном 5 минут
    guard = RiskGuard(cfg={"risk": {"cooldown_minutes": 5}})
    ctx = DummyCtx()

    # Первая сделка — должна пройти
    result1 = guard.check(ctx)
    assert result1 is True

    # Вторая сделка сразу — должна быть заблокирована кулдауном
    result2 = guard.check(ctx)
    assert result2 is False

    # Проверка: файл risk_blocks.csv должен существовать
    risk_blocks = logs_dir / "risk_blocks.csv"
    assert risk_blocks.exists()

    # Читаем последнюю строку
    with risk_blocks.open("r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) > 0
    last = rows[-1]

    # Проверяем поля
    assert last["symbol"] == "BTCUSDT"
    assert last["reason"] == "cooldown"
    assert "мин" in last["details"]  # должно содержать упоминание минут
    assert last["mode"] == "paper"
