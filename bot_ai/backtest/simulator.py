# simulator.py
# 🧪 Универсальный симулятор для любой стратегии

import pandas as pd
from bot_ai.data_loader import load_data

def simulate(pair, strategy_class, cfg, timeframe="1h"):
    df = load_data(pair, timeframe)
    strat = strategy_class(df, cfg)
    strat.generate_signals()
    return strat.get_dataframe()
