# telegram_alert.py
# Назначение: Отправка уведомлений в Telegram (с использованием .env)
# Структура:
# └── bot_ai/alerts/telegram_alert.py

from bot_ai.core.config_loader import get_env

def send_telegram(message):
    token = get_env("TELEGRAM_TOKEN")
    chat_id = get_env("TELEGRAM_CHAT_ID")
    print(f"📨 [Telegram] To {chat_id} via {token}: {message}")
