# ============================================
# File: bot_ai/run_grid_search.py
# Назначение: Расширенный перебор параметров стратегий
# Обновлено: Поддержка SL, TP, трейлинг, max_holding, R/R
# ============================================

import itertools
import pandas as pd
from bot_ai.strategy.strategy_loader import load_strategy
from bot_ai.data_loader import load_data
from bot_ai.metrics import calculate_metrics

def run_grid_search(strategy_name, symbol, param_grid, data_config, initial_balance=1000):
    df = load_data(symbol, **data_config)
    results = []

    keys, values = zip(*param_grid.items())
    for param_set in itertools.product(*values):
        params = dict(zip(keys, param_set))
        config = {"params": params}
        strategy = load_strategy(strategy_name, config)

        df_copy = df.copy()
        df_copy = strategy.calculate_indicators(df_copy)
        df_copy = strategy.generate_signals(df_copy)
        strategy.backtest(df_copy, initial_balance=initial_balance)

        summary = strategy.summary(symbol)
        if summary.empty:
            continue

        final_equity = summary["equity"].iloc[-1]
        metrics = calculate_metrics(summary)

        results.append({
            "params": params,
            "final_balance": final_equity,
            "sharpe": metrics.get("sharpe"),
            "drawdown": metrics.get("max_drawdown"),
            "win_rate": metrics.get("win_rate"),
            "profit_factor": metrics.get("profit_factor"),
            "trades": len(summary),
        })

    df_results = pd.DataFrame(results)
    df_results = df_results.sort_values(by="final_balance", ascending=False)
    df_results.to_csv(f"results/gridsearch_{strategy_name}_{symbol.replace('/', '')}.csv", index=False)
    return df_results
