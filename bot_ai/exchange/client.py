# bot_ai/exchange/client.py
# Binance API клиент для тестнета

from binance.client import Client
from config.config_loader import get_binance_credentials

class BinanceClient:
    def __init__(self):
        api_key, api_secret = get_binance_credentials()
        self.client = Client(api_key, api_secret)
        self.client.API_URL = "https://testnet.binance.vision/api"

    def buy(self, symbol, quantity):
        return self.client.create_order(
            symbol=symbol,
            side=Client.SIDE_BUY,
            type=Client.ORDER_TYPE_MARKET,
            quantity=quantity
        )

    def sell(self, symbol, quantity):
        return self.client.create_order(
            symbol=symbol,
            side=Client.SIDE_SELL,
            type=Client.ORDER_TYPE_MARKET,
            quantity=quantity
        )
