# snapshot_runner.py — с Telegram-уведомлением

import os
import datetime
from bot_ai.notifier.notifier import Notifier
from types import SimpleNamespace

# === ⚙️ Конфигурация уведомлений ===
cfg = SimpleNamespace(
    notifications={
        "enabled": True,
        "provider": "telegram",
        "telegram_token": "ВАШ_ТОКЕН",
        "telegram_chat_id": "ВАШ_CHAT_ID"
    }
)
notifier = Notifier(cfg)

# === 📸 Снимок проекта ===
now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
snapshot_path = "project_snapshot.txt"

with open(snapshot_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

summary_lines = [line for line in lines if line.startswith("## ") or line.startswith("- ")]
summary_text = "\n".join(summary_lines[:10])  # первые 10 строк

# === 📲 Telegram-уведомление ===
message = f"📸 <b>Снимок проекта</b>\nДата: {now}\nФайл: {snapshot_path}\n\n{summary_text}"
notifier.alert(message)
