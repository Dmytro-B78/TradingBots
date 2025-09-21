# tests/test_risk_guard_extended.py
# Расширенные тесты для RiskGuard:
# - Проверка кулдауна (cooldown_minutes)
# - Проверка лимита по количеству позиций (max_positions)
# - Проверка максимального размера позиции (max_position_size_pct)
# - Интеграционный тест: RiskGuard → TradeExecutor

import pytest
import time
from pathlib import Path

from bot_ai.risk.risk_guard import RiskGuard, TradeContext
from bot_ai.exec.executor import TradeExecutor


def make_ctx(**kwargs):
    """Упрощённый конструктор TradeContext с дефолтами"""
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


# === Проверка кулдауна ===
def test_risk_guard_cooldown_blocks_trades(monkeypatch):
    cfg = {"risk": {"cooldown_minutes": 5}}
    rg = RiskGuard(cfg)

    ctx = make_ctx()
    assert rg.check(ctx) is True  # первая сделка разрешена

    # monkeypatch time.time, чтобы имитировать "сразу после"
    monkeypatch.setattr(time, "time", lambda: rg.last_trade_time + 60)  # 1 минута спустя
    assert rg.check(ctx) is False  # блокировка из-за кулдауна


# === Проверка лимита по количеству позиций ===
def test_risk_guard_max_positions():
    cfg = {"risk": {"max_positions": 1}}
    rg = RiskGuard(cfg)
    rg.open_positions = 1

    ctx = make_ctx()
    assert rg.check(ctx) is False


# === Проверка максимального размера позиции ===
def test_risk_guard_max_position_size():
    cfg = {"risk": {"max_position_size_pct": 10}}  # максимум 10% от equity
    rg = RiskGuard(cfg)

    # Цена позиции = 2000, equity = 10_000 → 20% > 10%
    ctx = make_ctx(price=2000)
    assert rg.check(ctx) is False


# === Интеграционный тест: RiskGuard → TradeExecutor ===
def test_integration_risk_executor(tmp_path):
    cfg = {"risk": {"max_daily_loss_pct": 1}}
    rg = RiskGuard(cfg)
    executor = TradeExecutor(log_file=str(tmp_path / "trades.csv"))  # <-- исправлено

    # Сигнал "BUY" подставляем вручную
    ctx = make_ctx(daily_pnl_usdt=-500)  # -5% убыток при equity=10_000

    allowed = rg.check(ctx)
    if allowed:
        trade = {
            "symbol": ctx.symbol,
            "side": ctx.side,
            "price": ctx.price,
            "qty": 0.01,
        }
        executor.log_trade_to_csv(trade, signal_source="integration_test")

    # Проверяем, что сделка не попала в лог
    log_file = tmp_path / "trades.csv"
    if log_file.exists():
        content = log_file.read_text(encoding="utf-8")
        assert "BTCUSDT" not in content
    else:
        assert True  # файл даже не создан
