# ============================================
# 🧠 build_param_profiles.py
# --------------------------------------------
# Строит профили параметров под каждый режим
# Сохраняет в: profiles/trend.json, flat.json, volatile.json
# ============================================

import json
import os
import pandas as pd

# === 📥 Загрузка retrain-результатов ===
with open("results/retrain/best_params.json", "r", encoding="utf-8") as f:
    data = json.load(f)

df = pd.DataFrame(data)
df = df[df["regime"].notna()]
df["regime"] = df["regime"].str.lower()

# === 📁 Папка для профилей ===
output_dir = "profiles"
os.makedirs(output_dir, exist_ok=True)

# === 🧠 Функция: мода или медиана ===
def summarize_param(series):
    if series.dtype == int:
        return int(series.mode().iloc[0])
    return round(series.median(), 2)

# === 🔁 По каждому режиму ===
for regime in df["regime"].unique():
    subset = df[df["regime"] == regime]
    profile = {
        "regime": regime,
        "sma_fast": summarize_param(subset["fast_period"]),
        "sma_slow": summarize_param(subset["slow_period"]),
        "rsi_period": summarize_param(subset["rsi_period"]),
        "count": len(subset)
    }

    # 💾 Сохраняем профиль
    out_path = os.path.join(output_dir, f"{regime}.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(profile, f, indent=2, ensure_ascii=False)

    print(f"✅ Профиль сохранён: {out_path} ({profile['count']} примеров)")

print("\n🏁 Все профили построены.")
