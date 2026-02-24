# bot_ai/selector/pipeline_show_fix.py

import logging
import ccxt
from .pipeline_utils import _get_exchange_name

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def show_top_pairs(cfg, pairs, top_n=10, **kwargs):
    if not pairs:
        logger.info("Whitelist пуст — нечего отображать.")
        return False

    ex_class = getattr(ccxt, _get_exchange_name(cfg))
    ex = ex_class()

    for p in pairs[:top_n]:
        try:
            t = ex.fetch_ticker(p)
            volume = t.get("quoteVolume", 0)
            logger.info(f"{p}: volume={volume}")
            print(f"[SHOW] {p}: volume={volume}")  # 👈 отладочный вывод
        except Exception as e:
            logger.warning(f"{p}: ошибка при получении тикера: {e}")
            continue

    return False  # поведение по умолчанию
