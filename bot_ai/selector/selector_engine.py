# -*- coding: utf-8 -*-
# ============================================
# File: bot_ai/selector/selector_engine.py
# Purpose: Strategy selector engine
# ============================================

import pandas as pd
from typing import List, Union

from bot_ai.strategy.ma_crossover_strategy import ma_crossover_strategy

def run_selector(pair: str, df: pd.DataFrame, strategy_config: Union[str, dict]) -> List[dict]:
    if isinstance(strategy_config, dict):
        strategies = strategy_config.get("strategies", [])
        strategy_name = strategies[0] if strategies else None
    else:
        strategy_name = strategy_config

    if strategy_name in ("ma_crossover", "sma"):
        return ma_crossover_strategy(pair, df)
    else:
        print(f"[{pair}] Unknown strategy: {strategy_name}")
        return []
