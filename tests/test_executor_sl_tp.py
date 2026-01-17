from datetime import datetime

import pandas as pd
import pytz

from bot_ai.core.config import load_config
from bot_ai.exec.executor import TradeExecutor

prague_tz = pytz.timezone("Europe/Prague")

def main():
    cfg = load_config("config.json")
    executor = TradeExecutor(cfg)

    data = {
        "high": [
            105,
            106,
            107,
            108,
            109,
            110,
            111,
            112,
            113,
            114,
            115,
            116,
            117,
            118,
            119,
            120,
            121,
            122,
            123,
            124],
        "low": [
            95,
            96,
            97,
            98,
            99,
            100,
            101,
            102,
            103,
            104,
            105,
            106,
            107,
            108,
            109,
            110,
            111,
            112,
            113,
            114],
        "close": [
            100,
            101,
            102,
            103,
            104,
            105,
            106,
            107,
            108,
            109,
            110,
            111,
            112,
            113,
            114,
            115,
            116,
            117,
            118,
            119]}
    ohlcv_df = pd.DataFrame(data)

    trade_open = executor.execute_trade(
        symbol="BTC/USDT",
        side="long",
        price=110.0,
        ohlcv_df=ohlcv_df
    )
    trade_open["Time"] = datetime.now(prague_tz).strftime("%Y-%m-%d %H:%M:%S")
    print("\nОткрытие позиции:")
    print(trade_open)

    trade_close = executor.execute_trade(
        symbol="BTC/USDT",
        side="sell",
        price=115.0,
        ohlcv_df=ohlcv_df
    )
    trade_close["Time"] = datetime.now(prague_tz).strftime("%Y-%m-%d %H:%M:%S")
    print("\nЗакрытие позиции:")
    print(trade_close)

if __name__ == "__main__":
    main()

