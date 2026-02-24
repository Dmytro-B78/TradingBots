# ============================================
# File: bot_ai/optimize.py (обновление)
# Назначение: Автоматический выбор топ‑пар по объёму вместо whitelist.json
# ============================================

# ... (весь остальной код остаётся без изменений)

def get_top_symbols(exchange_client, limit=20):
    markets = exchange_client.load_markets()
    tickers = exchange_client.fetch_tickers()
    ranked = sorted(
        [s for s in tickers if "/USDT" in s and s in markets],
        key=lambda s: tickers[s].get("quoteVolume", 0),
        reverse=True
    )
    return ranked[:limit]

# === Основной запуск по всем парам из whitelist или топ‑объёму ===
def run_grid_search(cfg):
    exchange_client = get_exchange_client(cfg)
    timeframe = cfg["backtest"].get("timeframe", "1h")
    limit = cfg["backtest"].get("lookback_bars", 200)

    # Заменено: загрузка топ‑пар по объёму
    symbols = get_top_symbols(exchange_client, limit=20)

    fast_range = cfg["optimize"].get("sma_fast_range", [5, 10, 15])
    slow_range = cfg["optimize"].get("sma_slow_range", [20, 30, 40])
    rsi_range = cfg["optimize"].get("rsi_period_range", [10, 14, 20])

    all_results = []

    for symbol in symbols:
        try:
            ohlcv = exchange_client.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
            candles = [
                {"timestamp": o[0], "open": o[1], "high": o[2], "low": o[3], "close": o[4], "volume": o[5]}
                for o in ohlcv
            ]
            result = run_grid_optimization(symbol, fast_range, slow_range, rsi_range, candles)
            if result["best"]:
                all_results.append(result)
        except Exception as e:
            logger.warning(f"[ERROR] {symbol}: {e}")

    os.makedirs("results", exist_ok=True)
    with open("results/best_params.json", "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2)
    logger.info(f"[SAVE] Сохранены лучшие параметры {len(all_results)} пар в results/best_params.json")
