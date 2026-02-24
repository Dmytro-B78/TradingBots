# snapshot_runner.py РІР‚вЂќ РЎРѓ Telegram-РЎС“Р Р†Р ВµР Т‘Р С•Р СР В»Р ВµР Р…Р С‘Р ВµР С

import os
import datetime
from bot_ai.notifier.notifier import Notifier
from types import SimpleNamespace

# === РІС™в„ўРїС‘РЏ Р С™Р С•Р Р…РЎвЂћР С‘Р С–РЎС“РЎР‚Р В°РЎвЂ Р С‘РЎРЏ РЎС“Р Р†Р ВµР Т‘Р С•Р СР В»Р ВµР Р…Р С‘Р в„– ===
cfg = SimpleNamespace(
    notifications={
        "enabled": True,
        "provider": "telegram",
        "telegram_token": "Р вЂ™Р С’Р РЃ_Р СћР С›Р С™Р вЂўР Сњ",
        "telegram_chat_id": "Р вЂ™Р С’Р РЃ_CHAT_ID"
    }
)
notifier = Notifier(cfg)

# === СЂСџвЂњС‘ Р РЋР Р…Р С‘Р СР С•Р С” Р С—РЎР‚Р С•Р ВµР С”РЎвЂљР В° ===
now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
snapshot_path = "project_snapshot.txt"

with open(snapshot_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

summary_lines = [line for line in lines if line.startswith("## ") or line.startswith("- ")]
summary_text = "\n".join(summary_lines[:10])  # Р С—Р ВµРЎР‚Р Р†РЎвЂ№Р Вµ 10 РЎРѓРЎвЂљРЎР‚Р С•Р С”

# === СЂСџвЂњР† Telegram-РЎС“Р Р†Р ВµР Т‘Р С•Р СР В»Р ВµР Р…Р С‘Р Вµ ===
message = f"СЂСџвЂњС‘ <b>Р РЋР Р…Р С‘Р СР С•Р С” Р С—РЎР‚Р С•Р ВµР С”РЎвЂљР В°</b>\nР вЂќР В°РЎвЂљР В°: {now}\nР В¤Р В°Р в„–Р В»: {snapshot_path}\n\n{summary_text}"
notifier.alert(message)

