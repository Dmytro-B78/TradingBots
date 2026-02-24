# Скрипт для проверки совпадения сигналов с историческими свечами
# 1. Проходит по всем файлам test_signal_*.csv в папке paper_logs/
# 2. Преобразует entry_time в datetime и округляет до часа
# 3. Загружает соответствующий файл свечей из data/history/
# 4. Сравнивает, есть ли свеча с нужным временем
# 5. Показывает, какие сигналы не совпадают

import os
import pandas as pd

signals_dir = "paper_logs"
candles_dir = "data/history"

def check_signals_vs_candles(signal_path):
    df = pd.read_csv(signal_path)
    if "entry_time" not in df.columns or "symbol" not in df.columns:
        print(f"⚠️  Skipping {signal_path} — missing required columns.")
        return

    symbol = df["symbol"].iloc[0].replace("/", "")
    candle_file = os.path.join(candles_dir, f"{symbol}_1h.csv")
    if not os.path.exists(candle_file):
        print(f"⚠️  No candles found for {symbol}")
        return

    # Преобразуем entry_time в datetime и округляем до часа
    df["entry_time"] = pd.to_datetime(df["entry_time"], unit="ms").dt.floor("h")

    # Загружаем свечи
    candles = pd.read_csv(candle_file)
    candles["time"] = pd.to_datetime(candles["time"])

    # Сравниваем
    unmatched = df[~df["entry_time"].isin(candles["time"])]
    print(f"\n🔍 {symbol}: {len(unmatched)} unmatched of {len(df)} signals")

    # Показываем первые 5 несовпавших сигналов
    cols = [col for col in ["entry_time", "side", "entry_price"] if col in unmatched.columns]
    if not unmatched.empty and cols:
        print(unmatched[cols].head())
    elif unmatched.empty:
        print("✅ Все сигналы совпадают со свечами.")
    else:
        print("⚠️  Нет колонок side/entry_price для отображения.")

# Проходим по всем сигналам
for file in os.listdir(signals_dir):
    if file.startswith("test_signal_") and file.endswith("_signals.csv"):
        check_signals_vs_candles(os.path.join(signals_dir, file))
