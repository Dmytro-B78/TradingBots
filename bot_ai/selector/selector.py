# ============================================
# File: C:\TradingBots\NT\bot_ai\selector\selector.py
# Purpose: select_pairs — filters and selects trading pairs from Binance
# Encoding: UTF-8
# ============================================

def select_pairs(client, config):
    print("[SELECTOR] Fetching all symbols from exchange...")
    all_pairs = client.get_all_symbols()
    print(f"[SELECTOR] Total symbols: {len(all_pairs)}")

    filtered = []

    for symbol in all_pairs:
        try:
            ticker = client.get_24h_ticker(symbol)
            volume = float(ticker["quoteVolume"])
            spread = (float(ticker["askPrice"]) - float(ticker["bidPrice"])) / float(ticker["bidPrice"])
            volatility = (float(ticker["highPrice"]) - float(ticker["lowPrice"])) / float(ticker["openPrice"])

            if volume < config["risk"]["min_24h_volume_usdt"]:
                continue
            if spread > config["risk"]["max_spread_pct"] / 100:
                continue
            if volatility < config["risk"]["min_volatility"]:
                continue

            filtered.append({
                "symbol": symbol,
                "volume": volume,
                "spread": spread,
                "volatility": volatility
            })

        except Exception as e:
            print(f"[WARN] Skipping {symbol}: {e}")
            continue

    print(f"[SELECTOR] Pairs after filtering: {len(filtered)}")

    if not filtered:
        print("[SELECTOR] No pairs passed filters. Returning fallback: top 5 by volume")
        fallback = sorted(all_pairs, key=lambda s: float(client.get_24h_ticker(s)["quoteVolume"]), reverse=True)[:5]
        return fallback

    sorted_pairs = sorted(filtered, key=lambda x: x["volume"], reverse=True)
    top_n = config["risk"].get("top_n_pairs", 10)
    selected = [p["symbol"] for p in sorted_pairs[:top_n]]

    print(f"[SELECTOR] Selected pairs: {selected}")
    return selected
