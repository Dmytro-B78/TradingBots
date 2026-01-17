# -*- coding: utf-8 -*-
# ============================================
# File: bot_ai/selector/selector_engine.py
# Назначение: Запуск торговой стратегии и генерация сигналов
# ============================================

import pandas as pd
from typing import List

from strategies.ma_crossover import ma_crossover_strategy  # ✅ Исправленный импорт

def run_selector(pair: str, df: pd.DataFrame, strategy_name: str) -> List[dict]:
    """
    Запускает выбранную стратегию и возвращает список сигналов.
    :param pair: торговая пара, например "BTC/USDT"
    :param df: DataFrame с OHLCV-данными
    :param strategy_name: имя стратегии (например, "ma_crossover")
    :return: список сигналов (dict)
    """
    if strategy_name == "ma_crossover":
        return ma_crossover_strategy(pair, df)
    else:
        print(f"[{pair}] ⚠️ Неизвестная стратегия: {strategy_name}")
        return []
