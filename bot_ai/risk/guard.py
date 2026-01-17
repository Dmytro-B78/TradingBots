# ============================================
# File: bot_ai/risk/guard.py
# Purpose: Заглушка RiskGuard — пропускает все пары
# ============================================

class RiskGuard:
    def __init__(self, cfg):
        self.risk = cfg.get("risk", 0)

    def allow(self, pair):
        return True  # Пропускаем все пары без фильтрации

