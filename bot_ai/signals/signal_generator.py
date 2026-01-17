# bot_ai/signals/signal_generator.py
# Добавлена стратегия volume_rsi (объём + RSI)

from data.data_loader import fetch_data
import pandas as pd
import ta

def generate_signals(pair, timeframe, rsi_threshold=70, strategy="crossover", df=None, ema_fast=9, ema_slow=21):
    if df is None:
        df = fetch_data(pair, timeframe)

    if df is None or df.empty or len(df) < 3:
        print(f"⚠️ [{pair} | {strategy}] Недостаточно данных для сигнала")
        return []

    signals = []

    if strategy == "crossover":
        df["ema_fast"] = df["close"].ewm(span=ema_fast).mean()
        df["ema_slow"] = df["close"].ewm(span=ema_slow).mean()

        prev = df.iloc[-2]
        last = df.iloc[-1]

        if prev["ema_fast"] < prev["ema_slow"] and last["ema_fast"] > last["ema_slow"]:
            print(f"✅ [{pair} | crossover] BUY сигнал")
            signals.append("buy")
        elif prev["ema_fast"] > prev["ema_slow"] and last["ema_fast"] < last["ema_slow"]:
            print(f"✅ [{pair} | crossover] SELL сигнал")
            signals.append("sell")

    elif strategy == "volume_spike":
        df["vol_mean"] = df["volume"].rolling(window=20).mean()
        if df["vol_mean"].isna().all():
            print(f"⚠️ [{pair} | volume_spike] Недостаточно данных для среднего объёма")
            return []

        last_vol = df["volume"].iloc[-1]
        vol_avg = df["vol_mean"].iloc[-1]

        if last_vol > 1.2 * vol_avg:
            print(f"✅ [{pair} | volume_spike] BUY сигнал (объём {last_vol:.0f} > 1.2×{vol_avg:.0f})")
            signals.append("buy")

    elif strategy == "rsi":
        df["rsi"] = ta.momentum.RSIIndicator(df["close"], window=14).rsi()
        if df["rsi"].isna().all():
            print(f"⚠️ [{pair} | rsi] Недостаточно данных для RSI")
            return []

        last_rsi = df["rsi"].iloc[-1]
        if last_rsi < rsi_threshold:
            print(f"✅ [{pair} | rsi] BUY сигнал (RSI {last_rsi:.2f} < {rsi_threshold})")
            signals.append("buy")
        elif last_rsi > 100 - rsi_threshold:
            print(f"✅ [{pair} | rsi] SELL сигнал (RSI {last_rsi:.2f} > {100 - rsi_threshold})")
            signals.append("sell")

    elif strategy == "rsi_crossover":
        df["ema_fast"] = df["close"].ewm(span=ema_fast).mean()
        df["ema_slow"] = df["close"].ewm(span=ema_slow).mean()
        df["rsi"] = ta.momentum.RSIIndicator(df["close"], window=14).rsi()

        prev = df.iloc[-2]
        last = df.iloc[-1]

        if pd.notna(last["rsi"]) and pd.notna(prev["ema_fast"]) and pd.notna(prev["ema_slow"]):
            if last["rsi"] < rsi_threshold and prev["ema_fast"] < prev["ema_slow"] and last["ema_fast"] > last["ema_slow"]:
                print(f"✅ [{pair} | rsi_crossover] BUY сигнал (RSI {last['rsi']:.2f} < {rsi_threshold}) + EMA пересечение")
                signals.append("buy")
            elif last["rsi"] > 100 - rsi_threshold and prev["ema_fast"] > prev["ema_slow"] and last["ema_fast"] < last["ema_slow"]:
                print(f"✅ [{pair} | rsi_crossover] SELL сигнал (RSI {last['rsi']:.2f} > {100 - rsi_threshold}) + EMA пересечение")
                signals.append("sell")

    elif strategy == "volume_rsi":
        df["vol_mean"] = df["volume"].rolling(window=20).mean()
        df["rsi"] = ta.momentum.RSIIndicator(df["close"], window=14).rsi()

        if df["vol_mean"].isna().all() or df["rsi"].isna().all():
            print(f"⚠️ [{pair} | volume_rsi] Недостаточно данных для RSI или объёма")
            return []

        last = df.iloc[-1]
        vol_spike = last["volume"] > 1.2 * last["vol_mean"]

        if vol_spike and last["rsi"] < rsi_threshold:
            print(f"✅ [{pair} | volume_rsi] BUY сигнал (объём + RSI {last['rsi']:.2f} < {rsi_threshold})")
            signals.append("buy")
        elif vol_spike and last["rsi"] > 100 - rsi_threshold:
            print(f"✅ [{pair} | volume_rsi] SELL сигнал (объём + RSI {last['rsi']:.2f} > {100 - rsi_threshold})")
            signals.append("sell")

    if not signals:
        print(f"ℹ️ [{pair} | {strategy}] Сигналов нет")

    return signals
