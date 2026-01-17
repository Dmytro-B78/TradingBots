import logging
import os
from datetime import datetime, timedelta

import ccxt
import pandas as pd

def run_sma_backtest(cfg, pairs, days=30):
    logger = logging.getLogger(__name__)
    if not pairs:
        logger.warning("Список пар пуст — backtest не запущен.")
        return

    # Папка для результатов
    ts = datetime.utcnow().strftime("%Y%m%d_%H%M")
    results_dir = os.path.join("data", "backtests", ts)
    os.makedirs(results_dir, exist_ok=True)

    exchange_class = getattr(ccxt, cfg.exchange)
    exchange = exchange_class({'enableRateLimit': True})

    summary = []
    for symbol in pairs:
        try:
            since = exchange.parse8601(
                (datetime.utcnow() - timedelta(days=days)).isoformat())
            ohlcv = exchange.fetch_ohlcv(
                symbol, timeframe='1h', since=since, limit=days * 24)
            if not ohlcv:
                continue

            df = pd.DataFrame(
                ohlcv,
                columns=[
                    'time',
                    'open',
                    'high',
                    'low',
                    'close',
                    'volume'])
            df['SMA5'] = df['close'].rolling(window=5).mean()
            df['SMA20'] = df['close'].rolling(window=20).mean()

            position = None
            entry_price = 0
            trades = []

            for i in range(1, len(df)):
                if pd.isna(df['SMA5'].iloc[i]) or pd.isna(df['SMA20'].iloc[i]):
                    continue

                # BUY
                if df['SMA5'].iloc[i - 1] < df['SMA20'].iloc[i - \
                    1] and df['SMA5'].iloc[i] > df['SMA20'].iloc[i]:
                    if position != "LONG":
                        position = "LONG"
                        entry_price = df['close'].iloc[i]
                        trades.append(("BUY", df['time'].iloc[i], entry_price))

                # SELL
                elif df['SMA5'].iloc[i - 1] > df['SMA20'].iloc[i - 1] and df['SMA5'].iloc[i] < df['SMA20'].iloc[i]:
                    if position == "LONG":
                        exit_price = df['close'].iloc[i]
                        profit = (exit_price - entry_price) / entry_price * 100
                        trades.append(
                            ("SELL", df['time'].iloc[i], exit_price, profit))
                        position = None

            # Сохраняем сделки
            trades_df = pd.DataFrame(
                trades,
                columns=[
                    'Action',
                    'Time',
                    'Price',
                    'Profit(%)'])
            trades_file = os.path.join(
                results_dir, f"{
                    symbol.replace(
                        '/', '_')}_trades.csv")
            trades_df.to_csv(trades_file, index=False)

            total_profit = trades_df['Profit(%)'].sum(skipna=True)
            summary.append((symbol, len(trades_df) // 2, total_profit))

        except Exception as e:
            logger.warning(f"Ошибка backtest для {symbol}: {e}")

    # Сохраняем сводку
    summary_df = pd.DataFrame(
        summary,
        columns=[
            'Symbol',
            'Trades',
            'TotalProfit(%)'])
    summary_file = os.path.join(results_dir, "summary.csv")
    summary_df.to_csv(summary_file, index=False)

    logger.info(f"Backtest завершён. Результаты в {results_dir}")

