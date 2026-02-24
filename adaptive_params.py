# -*- coding: utf-8 -*-
# ============================================
# СЂСџвЂњвЂљ File: adaptive_params.py
# СЂСџВ§В  Р СњР В°Р В·Р Р…Р В°РЎвЂЎР ВµР Р…Р С‘Р Вµ: Р С›Р С—РЎР‚Р ВµР Т‘Р ВµР В»Р ВµР Р…Р С‘Р Вµ РЎР‚РЎвЂ№Р Р…Р С•РЎвЂЎР Р…Р С•Р С–Р С• РЎР‚Р ВµР В¶Р С‘Р СР В° Р С‘ Р В·Р В°Р С–РЎР‚РЎС“Р В·Р С”Р В° Р В°Р Т‘Р В°Р С—РЎвЂљР С‘Р Р†Р Р…РЎвЂ№РЎвЂ¦ Р С—Р В°РЎР‚Р В°Р СР ВµРЎвЂљРЎР‚Р С•Р Р†
# ============================================

import os
import json
import pandas as pd
from bot_ai.utils.market_regime import detect_market_regime

# === СЂСџвЂњТђ Р вЂ”Р В°Р С–РЎР‚РЎС“Р В·Р С”Р В° Р С—Р С•РЎРѓР В»Р ВµР Т‘Р Р…Р С‘РЎвЂ¦ РЎРѓР Р†Р ВµРЎвЂЎР ВµР в„– Р Т‘Р В»РЎРЏ Р В°Р Р…Р В°Р В»Р С‘Р В·Р В° ===
def load_recent_data(path="data/BTCUSDT_1h.csv", lookback=200):
    df = pd.read_csv(path)
    df["timestamp"] = pd.to_datetime(df["time"], unit="ms")
    df.set_index("timestamp", inplace=True)
    df.sort_index(inplace=True)
    return df.tail(lookback).reset_index(drop=True)

# === СЂСџВ§В  Р СџР С•Р В»РЎС“РЎвЂЎР ВµР Р…Р С‘Р Вµ Р В°Р Т‘Р В°Р С—РЎвЂљР С‘Р Р†Р Р…РЎвЂ№РЎвЂ¦ Р С—Р В°РЎР‚Р В°Р СР ВµРЎвЂљРЎР‚Р С•Р Р† Р С—Р С• РЎвЂљР ВµР С”РЎС“РЎвЂ°Р ВµР СРЎС“ РЎР‚Р ВµР В¶Р С‘Р СРЎС“ ===
def get_adaptive_params():
    df = load_recent_data()
    regime = detect_market_regime(df)
    profile_path = f"profiles/{regime}.json"

    if not os.path.exists(profile_path):
        raise FileNotFoundError(f"РІС™В РїС‘РЏ Р СџРЎР‚Р С•РЎвЂћР С‘Р В»РЎРЉ Р Р…Р Вµ Р Р…Р В°Р в„–Р Т‘Р ВµР Р…: {profile_path}")

    # РІСљвЂ¦ Р В§РЎвЂљР ВµР Р…Р С‘Р Вµ РЎРѓ Р С—Р С•Р Т‘Р Т‘Р ВµРЎР‚Р В¶Р С”Р С•Р в„– BOM
    with open(profile_path, "r", encoding="utf-8-sig") as f:
        params = json.load(f)

    print(f"СЂСџвЂњР‰ Р СћР ВµР С”РЎС“РЎвЂ°Р С‘Р в„– РЎР‚Р ВµР В¶Р С‘Р С: {regime.upper()} РІвЂ вЂ™ Р вЂ”Р В°Р С–РЎР‚РЎС“Р В¶Р ВµР Р… Р С—РЎР‚Р С•РЎвЂћР С‘Р В»РЎРЉ Р С—Р В°РЎР‚Р В°Р СР ВµРЎвЂљРЎР‚Р С•Р Р†")

    if "adaptive" not in params:
        raise KeyError(f"РІСњРЉ Р вЂ™ Р С—РЎР‚Р С•РЎвЂћР С‘Р В»Р Вµ {profile_path} Р С•РЎвЂљРЎРѓРЎС“РЎвЂљРЎРѓРЎвЂљР Р†РЎС“Р ВµРЎвЂљ Р С”Р В»РЎР‹РЎвЂЎ 'adaptive'. Р СњР В°Р в„–Р Т‘Р ВµР Р…Р С•: {list(params.keys())}")

    return {
        **params["adaptive"],
        "regime": regime
    }

