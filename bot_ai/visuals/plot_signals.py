# ============================================
# 📈 plot_signals.py — Визуализация сделок
# --------------------------------------------
# Функция:
# - Строит график свечей (OHLC)
# - Отмечает входы/выходы (buy/sell)
# - Рисует equity curve (если передана)
# Зависимости: matplotlib, mplfinance, pandas
# ============================================

import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf

def plot_signals_and_equity(df: pd.DataFrame, trades: list, equity: pd.Series = None):
    """
    Визуализация сигналов и equity curve

    Параметры:
    - df: DataFrame с OHLCV (индекс — datetime)
    - trades: список словарей с ключами:
        - entry_time, entry, direction, tp, sl, exit_time (опц.)
    - equity: Series с кумулятивной прибылью (опц.)

    Вывод:
    - График свечей с точками входа/выхода
    - Отдельный график equity curve (если передан)
    """
    df_plot = df.copy()
    df_plot.index.name = 'Date'

    # Списки для точек входа/выхода
    buys = []
    sells = []

    for trade in trades:
        entry_time = pd.to_datetime(trade["entry_time"])
        exit_time = pd.to_datetime(trade.get("exit_time", entry_time))
        direction = trade["direction"]

        if direction == "long":
            buys.append((entry_time, trade["entry"]))
            sells.append((exit_time, trade.get("exit", trade.get("tp"))))
        elif direction == "short":
            sells.append((entry_time, trade["entry"]))
            buys.append((exit_time, trade.get("exit", trade.get("tp"))))

    apds = []

    if buys:
        buy_df = pd.DataFrame(buys, columns=["Date", "Price"]).set_index("Date")
        apds.append(mpf.make_addplot(buy_df["Price"], type='scatter', markersize=100, marker='^', color='green'))

    if sells:
        sell_df = pd.DataFrame(sells, columns=["Date", "Price"]).set_index("Date")
        apds.append(mpf.make_addplot(sell_df["Price"], type='scatter', markersize=100, marker='v', color='red'))

    # График свечей с точками входа/выхода
    mpf.plot(
        df_plot,
        type='candle',
        style='yahoo',
        addplot=apds,
        volume=True,
        title="Signals and Trades",
        figratio=(16, 9),
        figscale=1.2
    )

    # Equity curve (если есть)
    if equity is not None:
        plt.figure(figsize=(12, 3))
        equity.plot(title="Equity Curve", grid=True, color="blue")
        plt.xlabel("Time")
        plt.ylabel("Equity")
        plt.tight_layout()
        plt.show()
