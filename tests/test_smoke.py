<<<<<<< HEAD
﻿# -*- coding: utf-8 -*-
# ============================================
# File: tests/test_smoke.py
# Назначение: Проверка базовой работоспособности проекта
# ============================================
=======
<<<<<<< Updated upstream
from bot_ai.core.config_loader import Config
from bot_ai.core.logger import get_logger
from bot_ai.utils.notifier import Notifier
from bot_ai.risk.risk_guard import RiskGuard, TradeContext
>>>>>>> 47a38855 (🔥 Финальный merge: stage0.4_main_release → main, конфликты решены)

from config.config_loader import get_binance_credentials

<<<<<<< HEAD
=======
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
=======
﻿# -*- coding: utf-8 -*-
# ============================================
# File: tests/test_smoke.py
# Назначение: Проверка базовой работоспособности проекта
# ============================================

from config.config_loader import get_binance_credentials

>>>>>>> 47a38855 (🔥 Финальный merge: stage0.4_main_release → main, конфликты решены)
def test_credentials_loaded():
    """
    Проверяет, что ключи Binance успешно загружаются из .env
    """
    api_key, api_secret = get_binance_credentials()
    assert api_key is not None and len(api_key) > 0
    assert api_secret is not None and len(api_secret) > 0
<<<<<<< HEAD
=======
>>>>>>> Stashed changes
>>>>>>> 47a38855 (🔥 Финальный merge: stage0.4_main_release → main, конфликты решены)
