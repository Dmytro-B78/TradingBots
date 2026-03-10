# ============================================
# File: bot_ai/core/context.py
# Purpose: MarketContext and TradeContext used across the system
# Format: UTF-8 without BOM
# ASCII only (no Cyrillic)
# ============================================

import pandas as pd
from datetime import datetime


class MarketContext:
    """
    MarketContext is used for strategy analysis (candles, indicators, etc.)
    """
    def __init__(self, df: pd.DataFrame, symbol: str, time: datetime, **kwargs):
        self.df = df
        self.symbol = symbol
        self.time = time
        self.extra = kwargs


class TradeContext:
    """
    TradeContext is used by RiskGuard and tests.
    It must contain specific fields expected by the test suite.
    """

    def __init__(
        self,
        symbol="BTCUSDT",
        daily_loss=0.0,
        vol24h_usdt=0.0,
        spread_pct=0.0,
        equity_usdt=0.0,
        price=0.0,
        mode="paper"
    ):
        self.symbol = symbol
        self.daily_loss = daily_loss
        self.vol24h_usdt = vol24h_usdt
        self.spread_pct = spread_pct
        self.equity_usdt = equity_usdt
        self.price = price
        self.mode = mode
