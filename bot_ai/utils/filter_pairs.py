# -*- coding: utf-8 -*-
# ============================================
# File: bot_ai/utils/filter_pairs.py
# Назначение: Фильтрация торговых пар по объёму, спреду и волатильности
# ============================================

import logging

def filter_pairs(pairs, client, cfg):
    """
    Фильтрует пары по объёму, спреду и волатильности.
    Возвращает список отфильтрованных пар.
    """
    filtered = []
    min_volume = cfg["risk"].get("min_24h_volume_usdt", 0)
    max_spread = cfg["risk"].get("max_spread_pct", 100)
    min_volatility = cfg["risk"].get("min_volatility", 0)

    for pair in pairs:
        try:
            ticker = client.fetch_ticker(pair["symbol"])
            volume = ticker.get("quoteVolume", 0)
            bid = ticker.get("bid", 0)
            ask = ticker.get("ask", 0)
            spread_pct = abs(ask - bid) / ask * 100 if ask else 100

            ohlcv = client.fetch_ohlcv(pair["symbol"], timeframe="1h", limit=10)
            closes = [c[4] for c in ohlcv]
            if len(closes) < 2:
                continue
            volatility = (max(closes) - min(closes)) / closes[-1]

            if volume >= min_volume and spread_pct <= max_spread and volatility >= min_volatility:
                filtered.append(pair)
            else:
                logging.info(f"[FILTER] {pair['symbol']} отклонена: volume={volume}, spread={spread_pct:.2f}%, vol={volatility:.4f}")
        except Exception as e:
            logging.warning(f"[FILTER] Ошибка при проверке {pair['symbol']}: {e}")
            continue

    logging.info(f"[FILTER] Пропущено: {len(filtered)} из {len(pairs)} пар")
    return filtered
