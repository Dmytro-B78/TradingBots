import pandas as pd

# Загрузка сигналов
signals = pd.read_csv("paper_logs/test_signal_AVAXUSDT_signals.csv")
signals["entry_time"] = pd.to_datetime(signals["entry_time"], unit="ms").dt.floor("h")

# Загрузка свечей
candles = pd.read_csv("data/history/AVAXUSDT_1h.csv")
candles["time"] = pd.to_datetime(candles["time"])

# Объединение по времени
merged = pd.merge(signals, candles, left_on="entry_time", right_on="time", how="left")

# Проверка исполнимости
def is_executable(row):
    price = row["price"]
    low = float(row["low"])
    high = float(row["high"])
    return low <= price <= high

merged["executable"] = merged.apply(is_executable, axis=1)

# Вывод результатов
total = len(merged)
ok = merged["executable"].sum()
fail = total - ok

print(f"\n📊 Исполнимо: {ok} из {total} сигналов")
print("\n❌ Неисполняемые сигналы:")
print(merged[~merged["executable"]][["entry_time", "signal", "price", "low", "high"]].head(10))
