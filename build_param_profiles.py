# ============================================
# СЂСџВ§В  build_param_profiles.py
# --------------------------------------------
# Р РЋРЎвЂљРЎР‚Р С•Р С‘РЎвЂљ Р С—РЎР‚Р С•РЎвЂћР С‘Р В»Р С‘ Р С—Р В°РЎР‚Р В°Р СР ВµРЎвЂљРЎР‚Р С•Р Р† Р С—Р С•Р Т‘ Р С”Р В°Р В¶Р Т‘РЎвЂ№Р в„– РЎР‚Р ВµР В¶Р С‘Р С
# Р РЋР С•РЎвЂ¦РЎР‚Р В°Р Р…РЎРЏР ВµРЎвЂљ Р Р†: profiles/trend.json, flat.json, volatile.json
# ============================================

import json
import os
import pandas as pd

# === СЂСџвЂњТђ Р вЂ”Р В°Р С–РЎР‚РЎС“Р В·Р С”Р В° retrain-РЎР‚Р ВµР В·РЎС“Р В»РЎРЉРЎвЂљР В°РЎвЂљР С•Р Р† ===
with open("results/retrain/best_params.json", "r", encoding="utf-8") as f:
    data = json.load(f)

df = pd.DataFrame(data)
df = df[df["regime"].notna()]
df["regime"] = df["regime"].str.lower()

# === СЂСџвЂњРѓ Р СџР В°Р С—Р С”Р В° Р Т‘Р В»РЎРЏ Р С—РЎР‚Р С•РЎвЂћР С‘Р В»Р ВµР в„– ===
output_dir = "profiles"
os.makedirs(output_dir, exist_ok=True)

# === СЂСџВ§В  Р В¤РЎС“Р Р…Р С”РЎвЂ Р С‘РЎРЏ: Р СР С•Р Т‘Р В° Р С‘Р В»Р С‘ Р СР ВµР Т‘Р С‘Р В°Р Р…Р В° ===
def summarize_param(series):
    if series.dtype == int:
        return int(series.mode().iloc[0])
    return round(series.median(), 2)

# === СЂСџвЂќРѓ Р СџР С• Р С”Р В°Р В¶Р Т‘Р С•Р СРЎС“ РЎР‚Р ВµР В¶Р С‘Р СРЎС“ ===
for regime in df["regime"].unique():
    subset = df[df["regime"] == regime]
    profile = {
        "regime": regime,
        "sma_fast": summarize_param(subset["fast_period"]),
        "sma_slow": summarize_param(subset["slow_period"]),
        "rsi_period": summarize_param(subset["rsi_period"]),
        "count": len(subset)
    }

    # СЂСџвЂ™С• Р РЋР С•РЎвЂ¦РЎР‚Р В°Р Р…РЎРЏР ВµР С Р С—РЎР‚Р С•РЎвЂћР С‘Р В»РЎРЉ
    out_path = os.path.join(output_dir, f"{regime}.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(profile, f, indent=2, ensure_ascii=False)

    print(f"РІСљвЂ¦ Р СџРЎР‚Р С•РЎвЂћР С‘Р В»РЎРЉ РЎРѓР С•РЎвЂ¦РЎР‚Р В°Р Р…РЎвЂР Р…: {out_path} ({profile['count']} Р С—РЎР‚Р С‘Р СР ВµРЎР‚Р С•Р Р†)")

print("\nСЂСџРЏРѓ Р вЂ™РЎРѓР Вµ Р С—РЎР‚Р С•РЎвЂћР С‘Р В»Р С‘ Р С—Р С•РЎРѓРЎвЂљРЎР‚Р С•Р ВµР Р…РЎвЂ№.")

