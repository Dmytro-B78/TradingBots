# ============================================
# File: notifier.py
# Purpose: Отправка уведомлений (Telegram)
# ============================================

import requests
import logging

class Notifier:
    def __init__(self, config):
        self.enabled = config.notifications.get("enabled", False)
        self.provider = config.notifications.get("provider", "telegram")
        self.token = config.notifications.get("telegram_token")
        self.chat_id = config.notifications.get("telegram_chat_id")

    def alert(self, message):
        if not self.enabled:
            return

        if self.provider == "telegram":
            self._send_telegram(message)
        else:
            logging.warning(f"[Notifier] Провайдер '{self.provider}' не поддерживается")

    def _send_telegram(self, message):
        if not self.token or not self.chat_id:
            logging.warning("[Notifier] Не указан токен или chat_id для Telegram")
            return

        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": "HTML"
        }

        try:
            response = requests.post(url, json=payload, timeout=10)
            if response.status_code != 200:
                logging.error(f"[Telegram] Ошибка отправки: {response.status_code} — {response.text}")
        except Exception as e:
            logging.error(f"[Telegram] Исключение при отправке: {e}")
