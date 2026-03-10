# ============================================
# File: bot_ai/core/trade_context.py
# Purpose: TradeContext used by RiskGuard and tests
# Format: UTF-8 without BOM
# ASCII only (no Cyrillic)
# ============================================

class TradeContext:
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
