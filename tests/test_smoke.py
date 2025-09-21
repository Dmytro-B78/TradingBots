from bot_ai.core.config_loader import Config
from bot_ai.core.logger import get_logger
from bot_ai.utils.notifier import Notifier
from bot_ai.risk.risk_guard import RiskGuard, TradeContext

def test_smoke():
    cfg = Config.load("config.json")
    logger = get_logger("smoke")

    notif_cfg = cfg.get("notifications", default={})
    notifier = Notifier(notif_cfg)  # создаём, но не передаём в RiskGuard

    guard = RiskGuard(cfg, logger)

    ctx = TradeContext(
        symbol="BTCUSDT",
        side="BUY",
        price=30000,
        equity_usdt=1000,
        daily_pnl_usdt=0,
        spread_pct=0.02,
        vol24h_usdt=50000000
    )

    assert guard.check(ctx) is True or guard.check(ctx) is False