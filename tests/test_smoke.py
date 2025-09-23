from bot_ai.core.config_loader import Config
from bot_ai.core.logger import get_logger
from bot_ai.utils.notifier import Notifier
from bot_ai.risk.risk_guard import RiskGuard, TradeContext

def test_smoke():
    # Загружаем конфиг
    cfg = Config.load("config.json")

    # Получаем логгер
    logger = get_logger("smoke")

    # Инициализируем Notifier (в ленивом режиме, без вызова send)
    notif_cfg = cfg.get("notifications", default={})
    notifier = Notifier(notif_cfg)

    # Инициализируем RiskGuard
    guard = RiskGuard(cfg, logger)

    # Создаём контекст сделки
    ctx = TradeContext(
        symbol="BTCUSDT",
        side="BUY",
        price=30000,
        equity_usdt=1000,
        daily_pnl_usdt=0,
        spread_pct=0.02,
        vol24h_usdt=50000000
    )

    # Проверяем RiskGuard
    result = guard.check(ctx)

    # Логируем результат для диагностики
    logger.info(f"[SMOKE] RiskGuard.check returned: {result}")

    # Утверждение: результат должен быть булевым
    assert isinstance(result, bool)
