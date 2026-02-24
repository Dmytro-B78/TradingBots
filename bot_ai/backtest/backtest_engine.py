# bot_ai/backtest/backtest_engine.py
# Исполняет сигналы, рассчитывает метрики, сохраняет лог сделок

import os
import pandas as pd
from bot_ai.backtest.simulator import Simulator

def run_backtest(pair, timeframe, strategy, rsi_threshold, capital, risk_pct):
    # Пути к файлам сигналов и исторических свечей
    signal_file = f"paper_logs/test_signal_{pair}_signals.csv"
    candle_file = f"data/history/{pair}_1h.csv"

    # Проверка наличия файлов
    if not os.path.exists(signal_file):
        print(f"❌ Нет сигналов: {signal_file}")
        return None
    if not os.path.exists(candle_file):
        print(f"❌ Нет свечей: {candle_file}")
        return None

    # Загрузка сигналов
    signals = pd.read_csv(signal_file)
    signals["entry_time"] = pd.to_datetime(signals["entry_time"], unit="ms").dt.floor("h")

    # Загрузка свечей
    candles = pd.read_csv(candle_file)
    candles["time"] = pd.to_datetime(candles["time"])

    # Инициализация симулятора
    sim = Simulator(
        initial_capital=capital,
        risk_per_trade=risk_pct,
        pair=pair,
        timeframe=timeframe
    )

    # Обработка сигналов
    for _, signal in signals.iterrows():
        entry_time = signal["entry_time"]
        side = signal["signal"].upper()
        entry_price = signal["price"]

        # Поиск свечи по времени
        candle = candles[candles["time"] == entry_time]
        if candle.empty:
            continue

        row = candle.iloc[0]
        low = float(row["low"])
        high = float(row["high"])

        # Проверка исполнимости сигнала
        if low <= entry_price <= high:
            sim.execute_trade(
                time=entry_time,
                side=side,
                price=entry_price
            )

    # Получение отчёта и сохранение сделок
    report, trades_df = sim.get_report()
    os.makedirs("logs", exist_ok=True)
    trades_df.to_csv("logs/trades.csv", index=False)

    return report
