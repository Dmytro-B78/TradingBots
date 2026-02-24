import os
import pandas as pd
import requests
from datetime import datetime, timedelta

INPUT_DIR = "paper_logs"
OUTPUT_DIR = "data/history"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_unique_symbols_and_min_time():
    symbols = set()
    min_time = None
    for file in os.listdir(INPUT_DIR):
        if file.endswith(".csv") and file.startswith("test_signal_"):
            df = pd.read_csv(os.path.join(INPUT_DIR, file))
            if "symbol" in df.columns and "entry_time" in df.columns:
                symbols.update(df["symbol"].unique())
                times = pd.to_datetime(df["entry_time"], unit="ms")
                tmin = times.min()
                if min_time is None or tmin < min_time:
                    min_time = tmin
    return sorted(symbols), min_time

def download_klines(symbol, start_date, end_date):
    binance_symbol = symbol.replace("/", "")
    start_ts = int(start_date.timestamp() * 1000)
    end_ts = int(end_date.timestamp() * 1000)

    url = "https://api.binance.com/api/v3/klines"
    params = {
        "symbol": binance_symbol,
        "interval": "1h",
        "startTime": start_ts,
        "endTime": end_ts,
        "limit": 1000
    }

    print(f"⬇️  Downloading {symbol} from {start_date.date()} to {end_date.date()}...")
    r = requests.get(url, params=params)
    if r.status_code != 200:
        print(f"  ❌ Failed to fetch {symbol}: {r.status_code} {r.text}")
        return

    data = r.json()
    if not data:
        print(f"  ⚠️ No data returned for {symbol}")
        return

    df = pd.DataFrame(data, columns=[
        "time", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "number_of_trades",
        "taker_buy_base", "taker_buy_quote", "ignore"
    ])
    df["time"] = pd.to_datetime(df["time"], unit="ms")
    df = df[["time", "open", "high", "low", "close"]]
    out_path = os.path.join(OUTPUT_DIR, f"{binance_symbol}_1h.csv")

    if os.path.exists(out_path):
        existing = pd.read_csv(out_path)
        existing["time"] = pd.to_datetime(existing["time"])
        df = pd.concat([existing, df]).drop_duplicates("time").sort_values("time")

    df.to_csv(out_path, index=False)
    print(f"  ✅ Saved to {out_path}")

if __name__ == "__main__":
    symbols, min_signal_time = get_unique_symbols_and_min_time()
    if not symbols or min_signal_time is None:
        print("⚠️ No valid signals found.")
    else:
        start_date = min_signal_time.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        end_date = datetime.utcnow() + timedelta(days=1)
        for s in symbols:
            download_klines(s, start_date, end_date)
