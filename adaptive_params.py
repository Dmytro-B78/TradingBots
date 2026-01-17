# -*- coding: utf-8 -*-
# ============================================
# 📂 File: adaptive_params.py
# 🧠 Назначение: Определение рыночного режима и загрузка адаптивных параметров
# ============================================

import os
import json
import pandas as pd
from bot_ai.utils.market_regime import detect_market_regime

# === 📥 Загрузка последних свечей для анализа ===
def load_recent_data(path="data/BTCUSDT_1h.csv", lookback=200):
    df = pd.read_csv(path)
    df["timestamp"] = pd.to_datetime(df["time"], unit="ms")
    df.set_index("timestamp", inplace=True)
    df.sort_index(inplace=True)
    return df.tail(lookback).reset_index(drop=True)

# === 🧠 Получение адаптивных параметров по текущему режиму ===
def get_adaptive_params():
    df = load_recent_data()
    regime = detect_market_regime(df)
    profile_path = f"profiles/{regime}.json"

    if not os.path.exists(profile_path):
        raise FileNotFoundError(f"⚠️ Профиль не найден: {profile_path}")

    # ✅ Чтение с поддержкой BOM
    with open(profile_path, "r", encoding="utf-8-sig") as f:
        params = json.load(f)

    print(f"📊 Текущий режим: {regime.upper()} → Загружен профиль параметров")

    if "adaptive" not in params:
        raise KeyError(f"❌ В профиле {profile_path} отсутствует ключ 'adaptive'. Найдено: {list(params.keys())}")

    return {
        **params["adaptive"],
        "regime": regime
    }
