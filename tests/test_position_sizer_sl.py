import pandas as pd

from bot_ai.core.config import load_config
from bot_ai.exec.executor import TradeExecutor

def calc_risk_usdt(entry_price, sl_price, position_size):
    if sl_price is None or position_size is None:
        return None
    stop_distance = abs(entry_price - sl_price)
    qty = position_size / entry_price
    return round(qty * stop_distance, 2)

def run_trade(executor, symbol, entry_price, sl_price):
    trade = executor.execute_trade(
        symbol=symbol,
        side="long",
        price=entry_price,
        ohlcv_df=ohlcv_df)
    trade["SL"] = sl_price
    trade["PositionSize"] = executor._calculate_position_size(
        entry_price, sl_price)
    risk = calc_risk_usdt(entry_price, sl_price, trade["PositionSize"])
    print(trade)
    print(f"Риск в $: {risk}")

# Фейковые OHLCV-данные
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

def main():
    cfg = load_config("config.json")

    print("\n=== Риск 1% — близкий стоп (SL=109) ===")
    executor = TradeExecutor(cfg)
    run_trade(executor, "BTC/USDT", 110.0, 109.0)

    print("\n=== Риск 1% — далёкий стоп (SL=90) ===")
    executor = TradeExecutor(cfg)
    run_trade(executor, "ETH/USDT", 110.0, 90.0)

    print("\n=== Риск 2% — близкий стоп (SL=109) ===")
    cfg.risk.risk_per_trade_pct = 2
    executor = TradeExecutor(cfg)
    run_trade(executor, "BNB/USDT", 110.0, 109.0)

if __name__ == "__main__":
    main()

