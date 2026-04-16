# ================================================================
# NT-Tech Night Backtest
# File: bot_ai/backtest/night_backtest.py
# Purpose: Run nightly batch backtest, ranking, summary output,
#          integrated Analyzer 2.2 per pair.
# ASCII-only
# ================================================================

import os
import json
from datetime import datetime

from bot_ai.selector.backtest_selector import fast_backtest
from bot_ai.selector.ranker import rank_pairs
from bot_ai.backtest.analyzer import analyze_backtest

CONFIG_PATH = "C:/TradingBots/NT/config.json"
LOG_PATH = "C:/TradingBots/logs/night_backtest.log"


def load_config():
    if not os.path.exists(CONFIG_PATH):
        raise FileNotFoundError("config.json not found")

    with open(CONFIG_PATH, "r") as f:
        return json.load(f)


def save_log(text: str):
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    with open(LOG_PATH, "a") as f:
        f.write(text + "\n")


def run_night_backtest():
    cfg = load_config()

    all_pairs = cfg.get("selector", {}).get("all_pairs", [])
    top_n = cfg.get("selector", {}).get("top_n", 3)
    candles_path = cfg.get("backtest", {}).get("candles_path", "C:/TradingBots/candles/compiled")
    lookback = cfg.get("backtest", {}).get("lookback_candles", 5000)

    if not all_pairs:
        raise ValueError("No pairs defined in config.json under selector.all_pairs")

    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    save_log("==============================================================")
    save_log(f"Night Backtest started: {timestamp}")
    save_log(f"Pairs: {len(all_pairs)}")
    save_log("==============================================================")

    # ------------------------------------------------------------
    # Run fast backtest for all pairs
    # ------------------------------------------------------------
    results = fast_backtest(
        symbols=all_pairs,
        candles_path=candles_path,
        lookback=lookback
    )

    # ------------------------------------------------------------
    # Run Analyzer 2.2 for each pair
    # ------------------------------------------------------------
    analysis = {}

    for symbol in all_pairs:
        data = results.get(symbol, {})
        trades = data.get("trades", [])
        risk = data.get("risk", [])

        report = analyze_backtest(trades, risk)
        analysis[symbol] = report

        save_log(f"[Analyzer] {symbol}: equity_end={report['equity_end']:.4f}, "
                 f"dd={report['max_drawdown']:.4f}, "
                 f"trades={report['trade_stats']['trades']}, "
                 f"winrate={report['trade_stats']['winrate']:.3f}, "
                 f"pf={report['trade_stats']['profit_factor']:.3f}, "
                 f"kills={report['kill_events']}")

    # ------------------------------------------------------------
    # Ranking
    # ------------------------------------------------------------
    ranked = rank_pairs(
        pairs=all_pairs,
        backtest_results=results,
        top_n=top_n
    )

    save_log("Ranking results:")
    for symbol, score, metrics in ranked:
        save_log(f"{symbol}: score={score}, metrics={metrics}")

    # ------------------------------------------------------------
    # Console summary
    # ------------------------------------------------------------
    print("==============================================================")
    print("NT-Tech Night Backtest Summary")
    print("==============================================================")

    for symbol, score, metrics in ranked:
        rep = analysis.get(symbol, {})
        ts = rep.get("trade_stats", {})

        print(f"{symbol:10s} | score={score:6.3f} | "
              f"pnl={metrics['avg_pnl']:.4f} | "
              f"win={metrics['winrate']:.3f} | "
              f"dd={metrics['max_dd']:.3f} | "
              f"trades={metrics['trades']} | "
              f"eq_end={rep.get('equity_end', 0):.2f} | "
              f"pf={ts.get('profit_factor', 0):.2f}")

    print("==============================================================")
    print("Done.")
    print("==============================================================")

    return ranked, analysis


if __name__ == "__main__":
    run_night_backtest()
