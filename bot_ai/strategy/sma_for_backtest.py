# ============================================
# bot_ai/strategy/sma_for_backtest.py
# Универсальная SMA-стратегия для live и backtest
# Возвращает либо сигнал ("buy"/"sell"), либо DataFrame сделок
# ============================================

import pandas as pd

def sma_strategy(df, live_mode=False, short_window=10, long_window=30):
    if df is None or df.empty:
        return None if live_mode else pd.DataFrame()

    # Расчёт скользящих средних
    df["SMA_Short"] = df["close"].rolling(window=short_window).mean()
    df["SMA_Long"] = df["close"].rolling(window=long_window).mean()

    if live_mode:
        # Возврат сигнала в live-режиме
        prev_short = df["SMA_Short"].iloc[-2]
        prev_long = df["SMA_Long"].iloc[-2]
        curr_short = df["SMA_Short"].iloc[-1]
        curr_long = df["SMA_Long"].iloc[-1]

        if pd.isna(prev_short) or pd.isna(prev_long) or pd.isna(curr_short) or pd.isna(curr_long):
            return None

        if prev_short < prev_long and curr_short > curr_long:
            return "buy"
        elif prev_short > prev_long and curr_short < curr_long:
            return "sell"
        else:
            return None
    else:
        # Генерация сделок для бэктеста
        trades = []
        position = 0
        for i in range(1, len(df)):
            prev_short = df["SMA_Short"].iloc[i - 1]
            prev_long = df["SMA_Long"].iloc[i - 1]
            curr_short = df["SMA_Short"].iloc[i]
            curr_long = df["SMA_Long"].iloc[i]

            if pd.isna(prev_short) or pd.isna(prev_long) or pd.isna(curr_short) or pd.isna(curr_long):
                continue

            if prev_short < prev_long and curr_short > curr_long and position <= 0:
                trades.append({
                    "Time": df["time"].iloc[i],
                    "Action": "BUY",
                    "Price": df["close"].iloc[i]
                })
                position = 1
            elif prev_short > prev_long and curr_short < curr_long and position >= 0:
                trades.append({
                    "Time": df["time"].iloc[i],
                    "Action": "SELL",
                    "Price": df["close"].iloc[i]
                })
                position = -1
        return pd.DataFrame(trades)

