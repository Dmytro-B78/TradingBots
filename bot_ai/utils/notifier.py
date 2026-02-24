# -*- coding: utf-8 -*-
# ============================================
# File: bot_ai/utils/notifier.py
# Назначение: Класс Notifier — отправка уведомлений (Telegram, консоль)
# ============================================

import logging
import requests

logger = logging.getLogger(__name__)

class Notifier:
    def __init__(self, config):
        # Поддержка как config.notifications, так и config напрямую
        cfg = getattr(config, "notifications", config)

        self.enabled = getattr(cfg, "enabled", False)
        self.provider = getattr(cfg, "provider", "console")
        self.token = getattr(cfg, "telegram_token", None)
        self.chat_id = getattr(cfg, "telegram_chat_id", None)

    def send(self, message: str):
        if not self.enabled:
            logger.info("Уведомления отключены.")
            return

        if self.provider == "telegram":
            try:
                response = requests.post(
                    f"https://api.telegram.org/bot{self.token}/sendMessage",
                    json={"chat_id": self.chat_id, "text": message}
                )
                if response.status_code != 200:
                    logger.warning(f"Ошибка отправки уведомления: {response.status_code} - {response.text}")
            except Exception as e:
                logger.warning(f"Ошибка отправки уведомления: {e}")
        elif self.provider == "console":
            logger.info(f"[NOTIFY] {message}")

    def trade_open(self, trade: dict):
        msg = f"Открыта сделка: {trade.get('Symbol')} {trade.get('Side')} по {trade.get('Price')} (SL: {trade.get('SL')}, TP: {trade.get('TP')})"
        self.send(msg)

    def trade_close(self, trade: dict):
        msg = f"Закрыта сделка: {trade.get('Symbol')} {trade.get('Side')} по {trade.get('Price')} | Прибыль: {trade.get('Profit(%)')}% / {trade.get('Profit(USDT)')} USDT"
        self.send(msg)

    def alert(self, message: str):
        self.send(f"[ALERT] {message}")
