# ============================================
# File: bot_ai/core/market_context.py
# Purpose: Wraps OHLCV DataFrame and metadata for strategy input
# ============================================

class MarketContext:
    def __init__(self, df, symbol, time):
        self.df = df
        self.symbol = symbol
        self.time = time
