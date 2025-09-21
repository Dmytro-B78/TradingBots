import logging
from bot_ai.core.config import load_config
from bot_ai.selector.pipeline import select_pairs
from bot_ai.risk.guard import RiskGuard
from bot_ai.utils.notifier import Notifier
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def main():
    start = time.time()
    cfg = load_config("config.json")
    notifier = Notifier(cfg)
    risk_guard = RiskGuard(cfg, notifier=notifier)

    pairs = select_pairs(cfg, risk_guard=risk_guard)

    print("\n=== РЕЗУЛЬТАТ ОТБОРА ПАР ===")
    for p in pairs:
        print(p)
    print(f"\nВсего отобрано: {len(pairs)} пар")
    print(f"Время выполнения: {time.time() - start:.2f} сек.")

if __name__ == "__main__":
    main()
