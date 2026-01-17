from datetime import datetime

import pytz

from bot_ai.core.config import load_config
from bot_ai.risk.guard import RiskGuard

prague_tz = pytz.timezone("Europe/Prague")

def main():
    cfg = load_config("config.json")
    rg = RiskGuard(cfg)

    print("\n=== ТЕСТ: фильтры по объёму и спреду ===")
    print("Объём ок?", rg.check_min_volume("BTC/USDT", 2_000_000))
    print("Спред ок?", rg.check_max_spread("BTC/USDT", 0.3))

    print("\n=== ТЕСТ: kill-switch ===")
    trades = [{"Time": datetime.now(prague_tz).strftime("%Y-%m-%d %H:%M:%S"),
               "Symbol": "BTC/USDT",
               "Profit(%)": -3,
               "Profit(USDT)": -30},
              {"Time": datetime.now(prague_tz).strftime("%Y-%m-%d %H:%M:%S"),
               "Symbol": "ETH/USDT",
               "Profit(%)": -4,
               "Profit(USDT)": -40},
              {"Time": datetime.now(prague_tz).strftime("%Y-%m-%d %H:%M:%S"),
               "Symbol": "BNB/USDT",
               "Profit(%)": -5,
               "Profit(USDT)": -50},
              ]
    for t in trades:
        rg.register_trade_result(t)
        print(f"Добавили сделку: {t['Symbol']} {t['Profit(%)']}%")
    if rg.kill_switch_triggered:
        print("Kill-switch сработал ? — торговля остановлена")

    print("\n=== ТЕСТ: cooldown ===")
    rg.start_cooldown(5)  # 5 секунд
    print("Cooldown активен?", rg.cooldown_active())

