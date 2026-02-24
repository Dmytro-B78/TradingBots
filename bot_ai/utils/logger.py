# Р В Р Р‹Р В РІР‚С™Р В Р Р‹Р РЋРЎСџР В Р вЂ Р В РІР‚С™Р РЋРЎв„ўР В Р’В Р РЋРІР‚Сљ bot_ai/utils/logger.py

import logging
import os

def init_logger(name="bot_ai", log_file="logs/bot.log", level=logging.INFO):
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(level)

    formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")

    # Р В Р’В Р вЂ™Р’В Р В Р Р‹Р Р†РІР‚С›РЎС›Р В Р’В Р вЂ™Р’В Р В Р Р‹Р Р†Р вЂљРЎС›Р В Р’В Р вЂ™Р’В Р В Р’В Р Р†Р вЂљР’В¦Р В Р’В Р В Р вЂ№Р В Р’В Р РЋРІР‚СљР В Р’В Р вЂ™Р’В Р В Р Р‹Р Р†Р вЂљРЎС›Р В Р’В Р вЂ™Р’В Р В РІР‚в„ўР вЂ™Р’В»Р В Р’В Р В Р вЂ№Р В Р’В Р В РІР‚В°
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # Р В Р’В Р вЂ™Р’В Р В РІР‚в„ўР вЂ™Р’В¤Р В Р’В Р вЂ™Р’В Р В РІР‚в„ўР вЂ™Р’В°Р В Р’В Р вЂ™Р’В Р В Р вЂ Р Р†Р вЂљРЎвЂєР Р†Р вЂљРІР‚СљР В Р’В Р вЂ™Р’В Р В РІР‚в„ўР вЂ™Р’В»
    fh = logging.FileHandler(log_file)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    return logger

