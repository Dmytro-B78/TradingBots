import csv
from pathlib import Path
from bot_ai.risk.guard import RiskGuard

class DummyCtx:
    def __init__(self, symbol="AVAXUSDT", vol24h_usdt=10000, spread_pct=1,
                 daily_pnl_usdt=100, equity_usdt=1000, price=50, mode="paper"):
        self.symbol = symbol
        self.vol24h_usdt = vol24h_usdt
        self.spread_pct = spread_pct
        self.daily_pnl_usdt = daily_pnl_usdt
        self.equity_usdt = equity_usdt
        self.price = price
        self.mode = mode

def test_pass_logging(tmp_path, monkeypatch):
    # Подготовка временной директории logs
    logs_dir = tmp_path / "logs"
    logs_dir.mkdir()
    monkeypatch.chdir(tmp_path)  # чтобы RiskGuard писал в tmp_path/logs

    # Конфиг с мягкими ограничениями, чтобы сделка прошла
    guard = RiskGuard(cfg={"risk": {
        "min_24h_volume_usdt": 100,
        "max_spread_pct": 10,
        "max_daily_loss_pct": 50,
        "kill_switch_loss_pct": 50,
        "max_positions": 10,
        "max_position_size_pct": 200,
        "cooldown_minutes": 0
    }})
    ctx = DummyCtx()

    # Действие: проверка сделки
    result = guard.check(ctx)

    # Проверка: сделка должна быть разрешена
    assert result is True

    # Проверка: файл risk_pass_log.csv должен существовать
    risk_pass = Path("risk_pass_log.csv")
    assert risk_pass.exists()

    # Читаем последнюю строку
    with risk_pass.open("r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) > 0
    last = rows[-1]

    # Проверяем поля
    assert "Сделка разрешена" in last["message"]
