# Patch get_data to return OHLCV data with deviation < -threshold
def mock_get_data(symbol, interval, lookback, source, **kwargs):
    sma_base = 100
    # 30 свечей около 100, затем 20 свечей с падением от 95 до 85
    prices = [sma_base + (i % 3 - 1) for i in range(30)] + [95 - i * 0.5 for i in range(20)]
    df = pd.DataFrame({
        "time": pd.date_range(start="2026-01-01", periods=50, freq="1h"),
        "open": prices,
        "high": [p + 0.5 for p in prices],
        "low": [p - 0.5 for p in prices],
        "close": prices,
        "volume": [10.0] * 50
    })
    return df
