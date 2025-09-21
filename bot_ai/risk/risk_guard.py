from dataclasses import dataclass
from .guard import RiskGuard

@dataclass
class TradeContext:
    symbol: str
    side: str
    price: float
    equity_usdt: float
    daily_pnl_usdt: float
    spread_pct: float
    vol24h_usdt: float
