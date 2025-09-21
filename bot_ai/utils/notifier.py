import logging
import requests
from types import SimpleNamespace

class Notifier:
    def __init__(self, cfg):
        self.cfg = cfg
        self.logger = logging.getLogger(__name__)

        notifications_cfg = getattr(cfg, "notifications", None)

        if isinstance(notifications_cfg, SimpleNamespace):
            self.enabled = getattr(notifications_cfg, "enabled", False)
            self.provider = getattr(notifications_cfg, "provider", "telegram")
            self.token = getattr(notifications_cfg, "telegram_token", "")
            self.chat_id = getattr(notifications_cfg, "telegram_chat_id", "")
        elif isinstance(notifications_cfg, dict):
            self.enabled = notifications_cfg.get("enabled", False)
            self.provider = notifications_cfg.get("provider", "telegram")
            self.token = notifications_cfg.get("telegram_token", "")
            self.chat_id = notifications_cfg.get("telegram_chat_id", "")
        else:
            self.enabled = False
            self.provider = "telegram"
            self.token = ""
            self.chat_id = ""

    def send(self, message: str):
        if not self.enabled:
            return

        if self.provider == "telegram" and self.token and self.chat_id:
            url = f"https://api.telegram.org/bot{self.token}/sendMessage"
            payload = {
                "chat_id": self.chat_id,
                "text": message,
                "parse_mode": "HTML"
            }
            try:
                resp = requests.post(url, data=payload, timeout=5)
                if resp.status_code != 200:
                    self.logger.error(f"Ошибка отправки в Telegram: {resp.text}")
            except Exception as e:
                self.logger.error(f"Ошибка при отправке уведомления: {e}")
        else:
            self.logger.info(f"[NOTIFY] {message}")

    def trade_open(self, trade_data: dict):
        msg = (
            f"📈 <b>Открыта позиция</b>\n"
            f"Символ: {trade_data.get('Symbol')}\n"
            f"Сторона: {str(trade_data.get('Side')).upper()}\n"
            f"Цена: {trade_data.get('Price')}\n"
            f"Размер: {trade_data.get('PositionSize')}\n"
            f"SL: {trade_data.get('SL')}\n"
            f"TP: {trade_data.get('TP')}"
        )
        self.send(msg)

    def trade_close(self, trade_data: dict):
        msg = (
            f"📉 <b>Закрыта позиция</b>\n"
            f"Символ: {trade_data.get('Symbol')}\n"
            f"Сторона: {str(trade_data.get('Side')).upper()}\n"
            f"Цена: {trade_data.get('Price')}\n"
            f"PnL: {trade_data.get('Profit(%)')}% ({trade_data.get('Profit(USDT)')} USDT)"
        )
        self.send(msg)

    def alert(self, text: str):
        self.send(f"⚠️ <b>АЛЕРТ</b>\n{text}")
