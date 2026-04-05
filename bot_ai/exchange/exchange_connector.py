# ================================================================
# File: bot_ai/exchange/exchange_connector.py
# Module: exchange.exchange_connector
# Purpose: NT-Tech unified exchange connector
# Responsibilities:
#   - Provide REST API wrapper
#   - Support authenticated requests
#   - Submit market and limit orders
#   - Query balances and positions
# Notes:
#   - ASCII-only
# ================================================================

import time
import hmac
import hashlib
import requests


class ExchangeConnector:
    """
    NT-Tech unified exchange connector (Binance-compatible).
    """

    def __init__(self, api_key, api_secret, base_url):
        self.api_key = api_key
        self.api_secret = api_secret.encode()
        self.base_url = base_url.rstrip("/")

    def _sign(self, params):
        query = "&".join([f"{k}={v}" for k, v in params.items()])
        signature = hmac.new(self.api_secret, query.encode(), hashlib.sha256).hexdigest()
        return signature

    def _headers(self):
        return {
            "X-MBX-APIKEY": self.api_key
        }

    def get(self, path, params=None):
        params = params or {}
        url = f"{self.base_url}{path}"
        r = requests.get(url, params=params, headers=self._headers(), timeout=10)
        return r.json()

    def post(self, path, params=None, signed=False):
        params = params or {}
        url = f"{self.base_url}{path}"

        if signed:
            params["timestamp"] = int(time.time() * 1000)
            params["signature"] = self._sign(params)

        r = requests.post(url, params=params, headers=self._headers(), timeout=10)
        return r.json()

    def account_info(self):
        return self.get("/api/v3/account")

    def ticker_price(self, symbol):
        return self.get("/api/v3/ticker/price", {"symbol": symbol})

    def order_market(self, symbol, side, quantity):
        return self.post(
            "/api/v3/order",
            {
                "symbol": symbol,
                "side": side,
                "type": "MARKET",
                "quantity": quantity
            },
            signed=True
        )

    def order_limit(self, symbol, side, quantity, price):
        return self.post(
            "/api/v3/order",
            {
                "symbol": symbol,
                "side": side,
                "type": "LIMIT",
                "timeInForce": "GTC",
                "quantity": quantity,
                "price": price
            },
            signed=True
        )
