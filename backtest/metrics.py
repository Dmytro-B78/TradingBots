# -*- coding: utf-8 -*-
# ============================================
# File: backtest/metrics.py
# Назначение: Расчёт метрик эффективности стратегии
# ============================================

import pandas as pd
import numpy as np

def calculate_metrics(trades: list, initial_balance: float = 10000.0):
    """
    Принимает список сделок и рассчитывает метрики:
    - итоговый баланс
    - общая доходность
    - волатильность
    - максимальная просадка
    - коэффициент Шарпа
    """
    if not trades:
        return {}

    balance = initial_balance
    equity_curve = [balance]

    for trade in trades:
        pnl = trade.get("pnl", 0)
        balance += pnl
        equity_curve.append(balance)

    returns = pd.Series(equity_curve).pct_change().dropna()
    total_return = (balance - initial_balance) / initial_balance
    volatility = returns.std()
    sharpe_ratio = returns.mean() / volatility * np.sqrt(252) if volatility > 0 else 0
    max_drawdown = calculate_max_drawdown(equity_curve)

    return {
        "final_balance": round(balance, 2),
        "total_return_pct": round(total_return * 100, 2),
        "volatility": round(volatility, 4),
        "sharpe_ratio": round(sharpe_ratio, 2),
        "max_drawdown_pct": round(max_drawdown * 100, 2)
    }

def calculate_max_drawdown(equity_curve: list):
    """
    Расчёт максимальной просадки по кривой капитала
    """
    curve = pd.Series(equity_curve)
    peak = curve.cummax()
    drawdown = (curve - peak) / peak
    return drawdown.min()
