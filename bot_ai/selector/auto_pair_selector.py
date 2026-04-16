# ================================================================
# NT-Tech Auto Pair Selector
# File: bot_ai/selector/auto_pair_selector.py
# Purpose: Select top trading pairs and update config.json
# ASCII-only
# ================================================================

import json
import os
from bot_ai.selector.ranker import rank_pairs
from bot_ai.selector.backtest_selector import fast_backtest


CONFIG_PATH = "C:/TradingBots/NT/config.json"


def load_config():
    if not os.path.exists(CONFIG_PATH):
        raise FileNotFoundError("config.json not found")

    with open(CONFIG_PATH, "r") as f:
        return json.load(f)


def save_config(cfg):
    with open(CONFIG_PATH, "w") as f:
        json.dump(cfg, f, indent=2)


def update_allowed_pairs():
    """
    Load config, run ranking, update allowed_pairs.
    """

    cfg = load_config()

    top_n = cfg.get("selector", {}).get("top_n", 3)
    all_pairs = cfg.get("selector", {}).get("all_pairs", [])

    if not all_pairs:
        raise ValueError("No pairs defined in config.json under selector.all_pairs")

    ranked = rank_pairs(
        pairs=all_pairs,
        backtest_results=None,
        fast_backtest_fn=fast_backtest,
        top_n=top_n
    )

    selected = [x[0] for x in ranked]

    cfg["allowed_pairs"] = selected

    save_config(cfg)

    return selected
