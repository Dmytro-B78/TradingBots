# ============================================
# 🪵 log.py — Логирование с префиксами
# --------------------------------------------
# Функции:
# - log_info(tag, msg):     [TAG] сообщение
# - log_warn(tag, msg):     [TAG][WARN] сообщение
# - log_error(tag, msg):    [TAG][ERROR] сообщение
# - log_debug(tag, msg):    [TAG][DEBUG] сообщение
# Поддержка цветного вывода (если терминал поддерживает)
# ============================================

import datetime

def _now():
    return datetime.datetime.now().strftime("%H:%M:%S")

def _format(tag, level, msg):
    return f"[{_now()}] [{tag.upper()}]{level} {msg}"

def log_info(tag, msg):
    print(_format(tag, "", msg))

def log_warn(tag, msg):
    print(_format(tag, "[WARN]", msg))

def log_error(tag, msg):
    print(_format(tag, "[ERROR]", msg))

def log_debug(tag, msg):
    print(_format(tag, "[DEBUG]", msg))
