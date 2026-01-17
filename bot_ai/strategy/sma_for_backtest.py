import pandas as pd

def sma_strategy(df, live_mode=False, short_window=10, long_window=30):
    if df is None or df.empty:
        return None if live_mode else pd.DataFrame()

    df['SMA_Short'] = df['close'].rolling(window=short_window).mean()
    df['SMA_Long'] = df['close'].rolling(window=long_window).mean()

    if live_mode:
        # Берём последние две свечи для определения сигнала
        if df['SMA_Short'].iloc[-2] < df['SMA_Long'].iloc[-2] and df['SMA_Short'].iloc[-1] > df['SMA_Long'].iloc[-1]:
            return "buy"
        elif df['SMA_Short'].iloc[-2] > df['SMA_Long'].iloc[-2] and df['SMA_Short'].iloc[-1] < df['SMA_Long'].iloc[-1]:
            return "sell"
        else:
            return None
    else:
        # Backtest-режим
        df['Signal'] = 0
        df.loc[df['SMA_Short'] > df['SMA_Long'], 'Signal'] = 1
        df.loc[df['SMA_Short'] < df['SMA_Long'], 'Signal'] = -1

        trades = []
        position = 0
        for i in range(1, len(df)):
            if df['Signal'].iloc[i] == 1 and position <= 0:
                trades.append(
                    {'Time': df['time'].iloc[i], 'Action': 'BUY', 'Price': df['close'].iloc[i]})
                position = 1
            elif df['Signal'].iloc[i] == -1 and position >= 0:
                trades.append(
                    {'Time': df['time'].iloc[i], 'Action': 'SELL', 'Price': df['close'].iloc[i]})
                position = -1
        return pd.DataFrame(trades)

