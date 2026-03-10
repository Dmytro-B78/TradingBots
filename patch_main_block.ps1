def main():
    symbols = load_whitelist()
    end_time = int(time.time() * 1000)
    start_time = int((datetime.utcnow() - timedelta(days=DAYS_BACK)).timestamp() * 1000)

    for entry in symbols:
        symbol = entry["symbol"]
        for interval in TIMEFRAMES:
            try:
                print(f"⬇️ Downloading: {symbol} | {interval}")
                klines = download_klines(symbol, interval, start_time, end_time)
                if klines:
                    save_klines(symbol, klines, interval)
                else:
                    print(f"⚠️ No data for {symbol} [{interval}]")
            except Exception as e:
                print(f"❌ Error {symbol} [{interval}]: {e}")
