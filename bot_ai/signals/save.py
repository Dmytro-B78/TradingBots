import json
import logging
import os

logger = logging.getLogger(__name__)

def save_signals(trades, symbol, strategy_name):
    if not trades:
        return
    os.makedirs("results", exist_ok=True)
    path = f"results/{symbol.replace('/', '_')}_{strategy_name}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(trades, f, indent=2, ensure_ascii=False)
    logger.info(f"[SAVE] РЎРёРіРЅР°Р»С‹ СЃРѕС…СЂР°РЅРµРЅС‹ РІ {path}")

