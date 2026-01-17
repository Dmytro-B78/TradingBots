# -*- coding: utf-8 -*-
# ============================================
# File: optimize.py
# Purpose: Подбор лучших параметров SMA/RSI
# Метод: Grid Search по PnL + экспорт в CSV
# ============================================

import os
import itertools
import logging
import pandas as pd

from bot_ai.strategy.mean_reversion import MeanReversionStrategy

# === 🧾 Логгер ===
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# === 🚀 Основная функция оптимизации ===
def optimize_parameters(
        pair,
        candles,
        sma_fast_range,
        sma_slow_range,
        rsi_range):
    """
    Перебор параметров SMA/RSI для стратегии Mean Reversion.
    Использует переданные свечи (candles).
    """
    best_score = float("-inf")
    best_params = None
    results = []

    df_raw = pd.DataFrame(candles)
    if df_raw.empty:
        logger.warning(f"[FAIL] {pair} — пустой набор свечей")
        return None

    for sma_fast, sma_slow, rsi_period in itertools.product(
            sma_fast_range, sma_slow_range, rsi_range):
        if sma_fast >= sma_slow:
            continue

        cfg = {
            "sma_fast": sma_fast,
            "sma_slow": sma_slow,
            "rsi_period": rsi_period
        }

        strategy = MeanReversionStrategy(cfg)
        df = df_raw.copy()

        df = strategy.calculate_indicators(df)
        df = strategy.generate_signals(df)
        strategy.backtest(df)
        trades = strategy.summary(pair)

        pnl = trades["pnl"].sum() if not trades.empty else 0
        logger.info(f"[GRID] {pair} | fast={sma_fast} slow={sma_slow} rsi={rsi_period} > PnL={pnl:.2f}")

        results.append({
            "pair": pair,
            "sma_fast": sma_fast,
            "sma_slow": sma_slow,
            "rsi_period": rsi_period,
            "pnl": round(pnl, 4)
        })

        if pnl > best_score:
            best_score = pnl
            best_params = {
                "fast_period": sma_fast,
                "slow_period": sma_slow,
                "rsi_period": rsi_period
            }

    if not results:
        logger.warning(f"[FAIL] {pair} — не удалось подобрать параметры")
        return None

    # === 💾 Сохраняем все результаты ===
    os.makedirs("results", exist_ok=True)
    df_all = pd.DataFrame(results)
    df_all.to_csv("results/grid_results.csv", index=False)
    logger.info(f"[EXPORT] Все комбинации сохранены в results/grid_results.csv")

    # === 💾 Сохраняем лучшие параметры ===
    best_row = df_all[df_all["pnl"] == df_all["pnl"].max()].iloc[0]
    df_best = pd.DataFrame([best_row])
    df_best.to_csv("results/best_params.csv", index=False)
    logger.info(f"[EXPORT] Лучшие параметры сохранены в results/best_params.csv")

    return best_params

# === 🔁 Обёртка для walk_forward.py ===
def run_grid_optimization(symbol, fast_periods, slow_periods, rsi_periods, candles):
    """
    Обёртка для использования в walk_forward.py
    """
    best = optimize_parameters(
        pair=symbol,
        candles=candles,
        sma_fast_range=fast_periods,
        sma_slow_range=slow_periods,
        rsi_range=rsi_periods
    )

    return {"best": best}
