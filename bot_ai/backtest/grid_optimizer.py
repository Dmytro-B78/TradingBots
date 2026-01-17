# bot_ai/backtest/grid_optimizer.py
# Финальное исправление: параметры передаются через cfg=params, как требует simulate()

from bot_ai.backtest.simulator import simulate
import pandas as pd
import os

def optimize_parameters(pair, timeframe, strategy, capital, risk_pct,
                        rsi_range=range(20, 50, 5),
                        ema_fast_range=None,
                        ema_slow_range=None,
                        bb_window_range=None,
                        bb_std_range=None,
                        min_trades=0,
                        sort_by="final_balance",
                        top_n=10):

    os.makedirs("results", exist_ok=True)
    results = []

    if strategy == "rsi_crossover":
        param_grid = [
            {"rsi_threshold": rsi, "ema_fast": ef, "ema_slow": es}
            for rsi in rsi_range
            for ef in ema_fast_range or []
            for es in ema_slow_range or []
            if es > ef
        ]
    elif strategy == "rsi_bbands":
        param_grid = [
            {"rsi_threshold": rsi, "bb_window": bw, "bb_std": bs}
            for rsi in rsi_range
            for bw in bb_window_range or []
            for bs in bb_std_range or []
        ]
    else:
        param_grid = [{"rsi_threshold": rsi} for rsi in rsi_range]

    total = len(param_grid)
    step = 1

    for params in param_grid:
        print(f"[{step}/{total}] {params}")
        step += 1

        df = simulate(
            pair=pair,
            timeframe=timeframe,
            strategy=strategy,
            capital=capital,
            risk_pct=risk_pct,
            cfg=params  # ✅ Параметры передаются как cfg
        )

        if df is None:
            print(f"⚠️ simulate() вернул None для {params}")
            continue
        if df.empty:
            print(f"⚠️ Пустой DataFrame для {params}")
            continue
        if len(df) < min_trades:
            print(f"⏭️ Пропущено: {params} → сделок={len(df)} < min_trades={min_trades}")
            continue

        wins = df[df["result"] == "TP"]
        losses = df[df["result"] == "SL"]
        winrate = round(len(wins) / len(df) * 100, 1) if len(df) > 0 else 0
        drawdown = round(df["balance"].max() - df["balance"].min(), 2)
        final_balance = df["balance"].iloc[-1]

        results.append({
            **params,
            "trades": len(df),
            "tp": len(wins),
            "sl": len(losses),
            "winrate": winrate,
            "final_balance": final_balance,
            "drawdown": drawdown
        })

    if results:
        df_results = pd.DataFrame(results)
        df_results.sort_values(by=sort_by, ascending=(sort_by == "drawdown"), inplace=True)
        path = f"results/gridsearch_{strategy}_{pair}.csv"
        df_results.to_csv(path, index=False)
        print(f"\n✅ Оптимизация завершена. Сохранено: {path}")
        print(df_results.head(top_n).to_string(index=False))
    else:
        print("❌ Нет результатов для сохранения.")
