# ================================================================
# NT-Tech Selector Backtest (Accelerated Model)
# File: bot_ai/selector/backtest_selector.py
# Purpose: Fast per-pair backtest for Selector using accelerated
#          trend-following model (EMA10/EMA30 + ATR7) and returning
#          real trades for Analyzer 2.2.
# ASCII-only
# ================================================================

import os
from glob import glob
import pandas as pd


def load_latest_csv(symbol: str, candles_path: str):
    """
    Load latest 1h CSV for symbol.
    Binance Vision CSV has no header, so we assign column names manually.
    """

    pattern = os.path.join(candles_path, f"{symbol}-1h-*.csv")
    files = glob(pattern)

    if not files:
        return None

    latest = sorted(files)[-1]

    try:
        df = pd.read_csv(
            latest,
            header=None,
            names=[
                "open_time",
                "open",
                "high",
                "low",
                "close",
                "volume",
                "close_time",
                "quote_volume",
                "trades",
                "taker_base",
                "taker_quote",
                "ignore"
            ]
        )
    except Exception:
        return None

    return df[["open", "high", "low", "close"]]


def run_accelerated_model(df: pd.DataFrame, lookback: int):
    """
    Accelerated trend-following model for Selector:
    - EMA fast = 10
    - EMA slow = 30
    - ATR = 7
    - Trend filter = 0.0005
    - Stop = 1.5 ATR
    - TP = 2.5 ATR
    """

    if df is None or len(df) < 200:
        return None

    df = df.tail(lookback).copy()

    close = df["close"]
    high = df["high"]
    low = df["low"]

    ema_fast_len = 10
    ema_slow_len = 30
    atr_len = 7

    df["ema_fast"] = close.ewm(span=ema_fast_len, adjust=False).mean()
    df["ema_slow"] = close.ewm(span=ema_slow_len, adjust=False).mean()

    tr1 = (high - low).abs()
    tr2 = (high - close.shift(1)).abs()
    tr3 = (low - close.shift(1)).abs()
    df["tr"] = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    df["atr"] = df["tr"].rolling(atr_len).mean()

    df = df.dropna().copy()
    if df.empty:
        return None

    position = 0
    entry_price = 0.0
    equity = [1.0]
    trade_returns = []

    stop_mult = 1.5
    tp_mult = 2.5
    trend_thr = 0.0005

    prev_ema_fast = df["ema_fast"].iloc[0]
    prev_ema_slow = df["ema_slow"].iloc[0]

    for idx, row in df.iterrows():
        price = float(row["close"])
        ema_fast = float(row["ema_fast"])
        ema_slow = float(row["ema_slow"])
        atr = float(row["atr"]) if row["atr"] == row["atr"] else 0.0

        eq = equity[-1]

        if position == 0:
            crossed_up = prev_ema_fast <= prev_ema_slow and ema_fast > ema_slow
            strong_trend = (ema_fast - ema_slow) / price > trend_thr

            if crossed_up and strong_trend and atr > 0:
                position = 1
                entry_price = price
                equity.append(eq)
            else:
                equity.append(eq)
        else:
            stop_price = entry_price - stop_mult * atr
            tp_price = entry_price + tp_mult * atr

            exit = False

            if price <= stop_price:
                exit = True
            elif price >= tp_price:
                exit = True
            elif ema_fast < ema_slow:
                exit = True

            if exit:
                ret = (price - entry_price) / entry_price
                trade_returns.append(ret)
                new_eq = eq * (1.0 + ret)
                equity.append(new_eq)
                position = 0
                entry_price = 0.0
            else:
                equity.append(eq)

        prev_ema_fast = ema_fast
        prev_ema_slow = ema_slow

    if not trade_returns:
        return None

    tr = pd.Series(trade_returns)

    avg_pnl = float(tr.mean())
    winrate = float((tr > 0).mean())

    eq = pd.Series(equity)
    roll_max = eq.cummax()
    dd = eq / roll_max - 1.0
    max_dd = float(dd.min())

    pos_sum = tr[tr > 0].sum()
    neg_sum = tr[tr < 0].sum()
    profit_factor = float(pos_sum / abs(neg_sum + 1e-12))

    try:
        stability = float(eq.corr(eq.expanding().mean()))
    except Exception:
        stability = 0.0

    # ------------------------------------------------------------
    # Build trade list for Analyzer 2.2
    # ------------------------------------------------------------
    trades_list = [
        {"pnl": float(ret), "day": "unknown"}
        for ret in trade_returns
    ]

    # No risk engine in accelerated model -> empty list
    risk_list = []

    return {
        "avg_pnl": round(avg_pnl, 4),
        "winrate": round(winrate, 4),
        "max_dd": round(max_dd, 4),
        "trades": trades_list,
        "risk": risk_list,
        "profit_factor": round(profit_factor, 4),
        "stability": round(stability, 4),
    }


def fast_backtest(symbols, candles_path="C:/TradingBots/candles/compiled", lookback=5000):
    """
    Run accelerated model backtest for list of symbols.
    """

    results = {}

    for symbol in symbols:
        df = load_latest_csv(symbol, candles_path)

        metrics = run_accelerated_model(df, lookback)

        if metrics is None:
            results[symbol] = {
                "avg_pnl": 0.0,
                "winrate": 0.0,
                "max_dd": 0.0,
                "trades": [],
                "risk": [],
                "profit_factor": 0.0,
                "stability": 0.0
            }
        else:
            results[symbol] = metrics

    return results
