# bot_ai/core/context.py

import pandas as pd
from datetime import datetime

class MarketContext:
    def __init__(self, df: pd.DataFrame, symbol: str, time: datetime, **kwargs):
        self.df = df
        self.symbol = symbol
        self.time = time
        self.extra = kwargs  # сюда можно передавать всё, что угодно (например, позицию, баланс и т.д.)

