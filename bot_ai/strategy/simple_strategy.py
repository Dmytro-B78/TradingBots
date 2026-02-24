import pandas as pd

# === Параметры стратегии ===
SHORT_WINDOW = 5     # короткая скользящая
LONG_WINDOW = 20     # длинная скользящая
MIN_SMA_DIFF = 0.002  # минимальное расхождение между SMA (0.2%)

def generate_signals(df):
    df = df.copy()
    df["sma_short"] = df["close"].rolling(window=SHORT_WINDOW).mean()
    df["sma_long"] = df["close"].rolling(window=LONG_WINDOW).mean()
    df["signal"] = None

    for i in range(1, len(df)):
        prev_short = df.loc[i - 1, "sma_short"]
        prev_long = df.loc[i - 1, "sma_long"]
        curr_short = df.loc[i, "sma_short"]
        curr_long = df.loc[i, "sma_long"]

        if pd.notna(prev_short) and pd.notna(prev_long) and pd.notna(curr_short) and pd.notna(curr_long):
            diff = abs(curr_short - curr_long) / curr_long
            if curr_short > curr_long and prev_short <= prev_long and diff >= MIN_SMA_DIFF:
                df.at[i, "signal"] = "buy"
            elif curr_short < curr_long and prev_short >= prev_long and diff >= MIN_SMA_DIFF:
                df.at[i, "signal"] = "sell"

    return df
