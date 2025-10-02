import csv
import pytest
from pathlib import Path
from bot_ai.exec.executor import TradeExecutor
from bot_ai.risk.risk_guard import RiskGuardWithLogging

def test_executor_blocks_trade_via_riskguard(tmp_path):
    log_file = tmp_path / "trades_log.csv"
    # RiskGuard с минимальным объёмом 1000 USDT
    rg = RiskGuardWithLogging(config={"risk": {"min_24h_volume_usdt": 1000}})
    executor = TradeExecutor(log_file=str(log_file), mode="paper", risk_guard=rg)

    # Сделка с объёмом меньше лимита — должна быть заблокирована
    trade = {
        "symbol": "BTCUSDT",
        "side": "BUY",
        "price": 27000.5,
        "qty": 0.01,
        "vol24h_usdt": 500,  # меньше лимита
        "equity_usdt": 1000,
        "daily_pnl_usdt": 0,
        "spread_pct": 0
    }

    with pytest.raises(PermissionError):
        executor.log_trade_to_csv(trade, signal_source="unit_test")

    # Лог пустой
    assert not Path(log_file).exists()

def test_executor_allows_trade_via_riskguard(tmp_path):
    log_file = tmp_path / "trades_log.csv"
    # Увеличили лимит размера позиции, чтобы сделка прошла
    rg = RiskGuardWithLogging(config={
        "risk": {
            "min_24h_volume_usdt": 100,
            "max_position_size_pct": 3000
        }
    })
    executor = TradeExecutor(log_file=str(log_file), mode="paper", risk_guard=rg)

    # Сделка проходит лимит
    trade = {
        "symbol": "BTCUSDT",
        "side": "BUY",
        "price": 27000.5,
        "qty": 0.01,
        "vol24h_usdt": 5000,
        "equity_usdt": 1000,
        "daily_pnl_usdt": 0,
        "spread_pct": 0
    }

    row = executor.log_trade_to_csv(trade, signal_source="unit_test")
    assert Path(log_file).exists()

    with open(log_file, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 1
    assert rows[0]["symbol"] == "BTCUSDT"
    assert rows[0]["signal_source"] == "unit_test"
