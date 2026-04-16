# ================================================================
# NT-Tech Selector Engine 2026
# File: bot_ai/selector/selector_engine.py
# Purpose:
#   - Provide class SelectorEngine for LiveEngine 4.3
#   - Provide full selector pipeline for cron/manual runs
# Pipeline:
#   screener -> fast_backtest -> ranker -> auto_pair_selector
# ASCII-only
# ================================================================

import json
import os
from datetime import datetime

from bot_ai.selector.screener import screen_pairs
from bot_ai.selector.backtest_selector import fast_backtest
from bot_ai.selector.ranker import rank_pairs
from bot_ai.selector.auto_pair_selector import update_allowed_pairs

CONFIG_PATH = "C:/TradingBots/NT/config.json"
LOG_PATH = "C:/TradingBots/logs/selector_engine.log"


# ================================================================
# SelectorEngine class (required by LiveEngine 4.3)
# ================================================================
class SelectorEngine:
    """
    Thin wrapper for LiveEngine 4.3.
    LiveEngine expects:
        selector = SelectorEngine(selector_cfg)
        pairs = selector.get_top_pairs()

    This class simply reads allowed_pairs from config.json,
    which are updated by auto_pair_selector.py.
    """

    def __init__(self, selector_cfg=None):
        self.selector_cfg = selector_cfg or {}

    def _load_config(self):
        if not os.path.exists(CONFIG_PATH):
            return {}
        try:
            with open(CONFIG_PATH, "r") as f:
                return json.load(f)
        except Exception:
            return {}

    def get_top_pairs(self):
        """
        Returns allowed_pairs from config.json.
        This is the authoritative output of the selector pipeline.
        """
        cfg = self._load_config()
        pairs = cfg.get("allowed_pairs", [])
        return list(pairs)


# ================================================================
# Helper functions for full selector pipeline
# ================================================================
def load_config():
    if not os.path.exists(CONFIG_PATH):
        raise FileNotFoundError("config.json not found")

    with open(CONFIG_PATH, "r") as f:
        return json.load(f)


def save_log(text: str):
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    with open(LOG_PATH, "a") as f:
        f.write(text + "\n")


# ================================================================
# Full selector pipeline (manual/cron)
# ================================================================
def run_selector_engine():
    """
    Full NT-Tech selector pipeline:
        1. Screen pairs
        2. Backtest screened pairs
        3. Rank pairs
        4. Update allowed_pairs in config.json
    """

    cfg = load_config()

    top_n = cfg.get("selector", {}).get("top_n", 3)
    candles_path = cfg.get("backtest", {}).get("candles_path", "C:/TradingBots/candles/compiled")
    lookback = cfg.get("backtest", {}).get("lookback_candles", 5000)

    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    save_log("==============================================================")
    save_log(f"Selector Engine started: {timestamp}")
    save_log("==============================================================")

    # Step 1: Screener
    screened = screen_pairs()
    save_log(f"Screened pairs: {len(screened)}")

    if not screened:
        save_log("No pairs passed screener")
        print("No pairs passed screener")
        return []

    # Step 2: Backtest
    results = fast_backtest(
        symbols=screened,
        candles_path=candles_path,
        lookback=lookback
    )

    # Step 3: Rank
    ranked = rank_pairs(
        pairs=screened,
        backtest_results=results,
        top_n=top_n
    )

    save_log("Ranking results:")
    for symbol, score, metrics in ranked:
        save_log(f"{symbol}: score={score}, metrics={metrics}")

    # Step 4: Update allowed_pairs
    selected = update_allowed_pairs()
    save_log(f"Updated allowed_pairs: {selected}")

    print("==============================================================")
    print("NT-Tech Selector Engine Summary")
    print("==============================================================")
    for symbol, score, metrics in ranked:
        print(f"{symbol:10s} | score={score:6.3f} | pnl={metrics['avg_pnl']:.4f} | win={metrics['winrate']:.3f} | dd={metrics['max_dd']:.3f} | trades={metrics['trades']}")

    print("==============================================================")
    print(f"Allowed pairs updated: {selected}")
    print("==============================================================")

    return ranked


# ================================================================
# CLI entry point
# ================================================================
if __name__ == "__main__":
    run_selector_engine()
