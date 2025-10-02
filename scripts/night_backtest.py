import sys, os

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

import pandas as pd
import matplotlib.pyplot as plt
from bot_ai.backtest import backtest_engine
from bot_ai.strategy.sma_for_backtest import sma_strategy
from bot_ai.strategy.rsi_for_backtest import rsi_strategy
from datetime import datetime
import logging
import numpy as np

os.makedirs("report", exist_ok=True)

logging.basicConfig(
    filename="report/night_backtest.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

cfg = type("Cfg", (), {})()
cfg.exchange = "binance"

pairs = ["BTC/USDT", "ETH/USDT", "BNB/USDT"]
print(f"Тестируем пары: {pairs}")

def calc_metrics(trades_df: pd.DataFrame):
    if trades_df is None or trades_df.empty:
        return {
            "profit_pct": 0.0,
            "max_drawdown": 0.0,
            "win_rate": 0.0,
            "avg_profit_per_trade": 0.0,
            "buy_count": 0,
            "sell_count": 0,
            "avg_trade_duration_h": 0.0
        }
    trades_df = trades_df.copy()
    if "Profit(%)" not in trades_df.columns and "Price" in trades_df.columns:
        trades_df["Profit(%)"] = trades_df["Price"].pct_change() * 100
        trades_df["Profit(%)"] = trades_df["Profit(%)"].fillna(0)
    profit_pct = trades_df["Profit(%)"].sum()
    equity_curve = trades_df["Profit(%)"].cumsum()
    max_drawdown = (equity_curve.cummax() - equity_curve).max()
    wins = (trades_df["Profit(%)"] > 0).sum()
    win_rate = wins / len(trades_df) * 100 if len(trades_df) > 0 else 0.0
    avg_profit_per_trade = trades_df["Profit(%)"].mean()
    buy_count = (trades_df["Action"] == "BUY").sum() if "Action" in trades_df.columns else 0
    sell_count = (trades_df["Action"] == "SELL").sum() if "Action" in trades_df.columns else 0
    avg_trade_duration_h = 0.0
    if "Time" in trades_df.columns:
        times = pd.to_datetime(trades_df["Time"])
        if len(times) > 1:
            durations = times.diff().dt.total_seconds() / 3600
            avg_trade_duration_h = durations.mean()
    return {
        "profit_pct": round(float(profit_pct), 2),
        "max_drawdown": round(float(max_drawdown), 2),
        "win_rate": round(float(win_rate), 2),
        "avg_profit_per_trade": round(float(avg_profit_per_trade), 2),
        "buy_count": int(buy_count),
        "sell_count": int(sell_count),
        "avg_trade_duration_h": round(float(avg_trade_duration_h), 2)
    }

def plot_monthly_distribution(trades_df: pd.DataFrame, strategy_name: str, pair: str):
    if trades_df is None or trades_df.empty or "Time" not in trades_df.columns:
        return None, None, None
    trades_df = trades_df.copy()
    trades_df["Month"] = pd.to_datetime(trades_df["Time"]).dt.to_period("M")
    if "Profit(%)" not in trades_df.columns and "Price" in trades_df.columns:
        trades_df["Profit(%)"] = trades_df["Price"].pct_change() * 100
        trades_df["Profit(%)"] = trades_df["Profit(%)"].fillna(0)
    monthly_profit = trades_df.groupby("Month")["Profit(%)"].sum()
    monthly_drawdown = trades_df.groupby("Month")["Profit(%)"].apply(
        lambda profit: (profit.cumsum().cummax() - profit.cumsum()).mean()
    )
    plt.figure(figsize=(8,4))
    monthly_profit.plot(kind="bar", color="skyblue")
    plt.title(f"Monthly Profit Distribution - {strategy_name} {pair}")
    plt.ylabel("Profit (%)")
    plt.tight_layout()
    img_path = f"report/{strategy_name}_{pair.replace('/','_')}_monthly_profit.png"
    plt.savefig(img_path)
    plt.close()
    return img_path, monthly_profit, monthly_drawdown

def plot_equity_curve(trades_df: pd.DataFrame, strategy_name: str, pair: str):
    if trades_df is None or trades_df.empty or "Profit(%)" not in trades_df.columns:
        return None
    plt.figure(figsize=(8,4))
    trades_df["Profit(%)"].cumsum().plot(color="green")
    plt.title(f"Equity Curve - {strategy_name} {pair}")
    plt.ylabel("Cumulative Profit (%)")
    plt.tight_layout()
    img_path = f"report/{strategy_name}_{pair.replace('/','_')}_equity_curve.png"
    plt.savefig(img_path)
    plt.close()
    return img_path

results = []
html_parts = []

for strat_name, strat_fn in [("SMA", sma_strategy), ("RSI", rsi_strategy)]:
    for pair in pairs:
        print(f"\n=== {strat_name} {pair} ===")
        trades_df = backtest_engine.run_backtest(
            cfg,
            [pair],
            strat_fn,
            strat_name,
            days=365,
            timeframes=["1h", "4h", "1d"]
        )
        if trades_df is not None and not trades_df.empty:
            metrics = calc_metrics(trades_df)
            metrics["Strategy"] = strat_name
            metrics["Pair"] = pair
            results.append(metrics)
            monthly_img, monthly_profit, monthly_drawdown = plot_monthly_distribution(trades_df, strat_name, pair)
            equity_img = plot_equity_curve(trades_df, strat_name, pair)
            html_parts.append(f"<h2>{strat_name} - {pair}</h2>")
            html_parts.append(pd.DataFrame([metrics]).to_html(index=False))
            if monthly_img:
                html_parts.append(f'<img src="{monthly_img}" alt="Monthly Profit">')
                html_parts.append("<h3>Средняя прибыль по месяцам</h3>")
                html_parts.append(monthly_profit.to_frame(name="Profit(%)").to_html())
                html_parts.append("<h3>Средняя просадка по месяцам</h3>")
                html_parts.append(monthly_drawdown.to_frame(name="Drawdown(%)").to_html())
            if equity_img:
                html_parts.append(f'<img src="{equity_img}" alt="Equity Curve">')
        else:
            print(f"{pair}: нет сделок")

# Сводная таблица с рангом и подсветкой
summary_df = pd.DataFrame(results).sort_values(by="profit_pct", ascending=False)
summary_df.insert(0, "Rank", range(1, len(summary_df) + 1))

def highlight_rows(row):
    if row["Rank"] <= 3:
        return ['background-color: lightgreen'] * len(row)
    elif row["Rank"] > len(summary_df) - 3:
        return ['background-color: lightcoral'] * len(row)
    else:
        return [''] * len(row)

styled_html = summary_df.style.apply(highlight_rows, axis=1).to_html()

html_parts.insert(0, "<h1>Сводная таблица по всем стратегиям и парам (с рейтингом)</h1>")
html_parts.insert(1, styled_html)

summary_df.to_csv("report/night_backtest_summary.csv", index=False, encoding="utf-8")

with open("report/night_backtest.html", "w", encoding="utf-8") as f:
    f.write("<html><body>")
    f.write("".join(html_parts))
    f.write("</body></html>")

print("\nБэктест завершён:", datetime.now())
print("Сводный отчёт сохранён в report/night_backtest_summary.csv и report/night_backtest.html")
