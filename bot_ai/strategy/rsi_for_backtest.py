import pandas as pd

def rsi_strategy(df, live_mode=False, period=14, overbought=70, oversold=30):
    if df is None or df.empty:
        return None if live_mode else pd.DataFrame()

    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))

    if live_mode:
        last_rsi = df['RSI'].iloc[-1]
        if last_rsi < oversold:
            return "buy"
        elif last_rsi > overbought:
            return "sell"
        else:
            return None
    else:
        trades = []
        position = 0
        for i in range(1, len(df)):
            if df['RSI'].iloc[i] < oversold and position <= 0:
                trades.append({'Time': df['time'].iloc[i], 'Action': 'BUY', 'Price': df['close'].iloc[i]})
                position = 1
            elif df['RSI'].iloc[i] > overbought and position >= 0:
                trades.append({'Time': df['time'].iloc[i], 'Action': 'SELL', 'Price': df['close'].iloc[i]})
                position = -1
        return pd.DataFrame(trades)
