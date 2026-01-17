import csv

from bot_ai.risk.guard import RiskGuard

class DummyCtx:
    def __init__(self, symbol="BTCUSDT", vol24h_usdt=0, spread_pct=0,
                 daily_pnl_usdt=0, equity_usdt=1000, price=100, mode="paper"):
        self.symbol = symbol
        self.vol24h_usdt = vol24h_usdt
        self.spread_pct = spread_pct
        self.daily_pnl_usdt = daily_pnl_usdt
        self.equity_usdt = equity_usdt
        self.price = price
        self.mode = mode

def test_low_volume_block(tmp_path, monkeypatch):
    # Подготовка временной директории logs
    logs_dir = tmp_path / "logs"
    logs_dir.mkdir()
    monkeypatch.chdir(tmp_path)  # чтобы RiskGuard писал в tmp_path/logs

    # Конфиг с минимальным объёмом
    guard = RiskGuard(cfg={"risk": {"min_24h_volume_usdt": 1000}})
    ctx = DummyCtx(vol24h_usdt=10)

    # Действие: проверка сделки
    result = guard.check(ctx)

    # Проверка: сделка должна быть заблокирована
    assert result is False

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
    assert last["reason"] == "low_volume"
    assert "10" in last["details"]  # должно содержать фактический объём
    assert last["mode"] == "paper"

