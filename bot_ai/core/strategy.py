# bot_ai/core/strategy.py
# 🧠 Базовый класс стратегии с поддержкой режима работы

import pandas as pd

class Strategy:
    def __init__(self, df: pd.DataFrame, config: dict, mode: str = "backtest"):
        self.df = df.copy()         # ✅ сохраняем датафрейм
        self.config = config        # ✅ сохраняем конфиг
        self.mode = mode            # "backtest", "live", "paper"
        self.df["signal"] = 0       # инициализируем колонку сигналов

    def generate_signals(self):
        raise NotImplementedError("Метод generate_signals() должен быть реализован в подклассе.")

    def get_dataframe(self):
        return self.df

    def is_live(self):
        return self.mode == "live"

    def is_backtest(self):
        return self.mode == "backtest"

    def is_paper(self):
        return self.mode == "paper"
