# ================================================================
# NT-Tech Ranker
# File: bot_ai/selector/ranker.py
# Purpose: Rank trading pairs based on backtest metrics.
# ASCII-only
# ================================================================

import math


def compute_score(metrics: dict):
    """
    Compute composite score for a single symbol.
    Metrics dict contains:
        avg_pnl
        winrate
        max_dd
        trades  (can be int or list of trades)
        profit_factor
        stability
    """

    trades_raw = metrics.get("trades", 0)

    if isinstance(trades_raw, list):
        trades_count = len(trades_raw)
    else:
        try:
            trades_count = int(trades_raw)
        except Exception:
            trades_count = 0

    if trades_count == 0:
        return 0.0

    avg_pnl = metrics.get("avg_pnl", 0.0)
    winrate = metrics.get("winrate", 0.0)
    max_dd = metrics.get("max_dd", 0.0)
    profit_factor = metrics.get("profit_factor", 0.0)
    stability = metrics.get("stability", 0.0)

    score = 0.0
    score += avg_pnl * 2.0
    score += winrate * 1.5
    score += profit_factor * 1.2
    score += stability * 1.0
    score += min(trades_count / 200.0, 1.0) * 0.5
    score += max_dd * -1.5

    return round(score, 6)


def rank_pairs(pairs: list, backtest_results: dict = None, fast_backtest_fn=None, top_n: int = 10):
    """
    Rank pairs using:
        - provided backtest_results
        - or fast_backtest_fn if results not provided
    """

    if backtest_results is None:
        if fast_backtest_fn is None:
            raise ValueError("fast_backtest_fn is required when backtest_results is None")
        backtest_results = fast_backtest_fn(pairs)

    scored = []

    for symbol in pairs:
        metrics = backtest_results.get(symbol, None)
        if metrics is None:
            continue

        score = compute_score(metrics)
        scored.append((symbol, score, metrics))

    scored_sorted = sorted(scored, key=lambda x: x[1], reverse=True)

    return scored_sorted[:top_n]
