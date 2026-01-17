# Исправляем вызов cfg.get(...) — передаём default как именованный аргумент
# Это устраняет ошибку TypeError при запуске smoke-теста

self.risk_cfg = cfg.get("risk", default={})

