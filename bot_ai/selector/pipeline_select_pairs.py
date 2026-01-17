# ============================================
# File: bot_ai/selector/pipeline_select_pairs.py
# Назначение: Автоматический выбор торговых пар с определением рыночного режима и стратегии
# ============================================

import logging

import ccxt

from bot_ai.risk.risk_guard import TradeContext
from bot_ai.selector.trend_utils import detect_regime

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def select_pairs(cfg, risk_guard=None, use_cache=True):
    """
    Загружает список всех рынков с биржи и фильтрует их по условиям из config.json.
    Возвращает список словарей: {pair, regime, strategy}
    """

    ex_class = getattr(ccxt, cfg.get("exchange", "binance"))
    ex = ex_class()

    try:
        markets = ex.load_markets()
    except Exception as e:
        logger.error(f"Ошибка загрузки рынков: {e}")
        return []

    pairs = [p for p in markets.keys() if p.endswith("/USDT")]
    selected = []

    min_vol = cfg["risk"].get("min_24h_volume_usdt", 0)
    max_spread = cfg["risk"].get("max_spread_pct", 100)
    min_price = cfg["risk"].get("min_price_usdt", 0.1)
    min_volatility = 0.005
    tf = cfg["pair_selection"].get("d1_timeframe", "1d")

    for pair in pairs:
        try:
            ticker = ex.fetch_ticker(pair)
            vol = ticker.get("quoteVolume", 0)
            ask = ticker.get("ask", None)
            bid = ticker.get("bid", None)
            last_price = ticker.get("last", 0)
            high = ticker.get("high", 0)
            low = ticker.get("low", 0)
            close = ticker.get("close", last_price)

            # Фильтр по объёму
            if vol is None or vol < min_vol:
                continue

            # Фильтр по цене
            if last_price < min_price:
                continue

            # Фильтр по спреду
            if ask and bid and bid > 0:
                spread_pct = (ask - bid) / bid * 100
                if spread_pct > max_spread:
                    continue

            # Фильтр по волатильности
            if close == 0 or high == 0 or low == 0:
                continue
            volatility = (high - low) / close
            if volatility < min_volatility:
                continue

            # RiskGuard
            if risk_guard:
                ctx = TradeContext(
                    symbol=pair,
                    side="long",
                    price=last_price,
                    equity_usdt=cfg["risk"]["test_equity"],
                    daily_pnl_usdt=0,
                    spread_pct=spread_pct if ask and bid else 0,
                    vol24h_usdt=vol
                )
                if not risk_guard.check(ctx):
                    continue

            # Определение режима
            try:
                regime = detect_regime(ex, pair, tf=tf)
            except Exception as e:
                logger.warning(f"{pair}: ошибка определения режима: {e}")
                regime = "unknown"

            # Назначение стратегии
            strategy = None
            if regime == "uptrend":
                strategy = "adaptive"
            elif regime == "range":
                strategy = "countertrend"
            elif regime == "volatile":
                strategy = "breakout"

            if strategy:
                selected.append({
                    "pair": pair,
                    "regime": regime,
                    "strategy": strategy
                })
                logger.info(
                    f"{pair}: принято — режим {regime}, стратегия {strategy}")
            else:
                logger.info(
                    f"{pair}: отклонено — режим {regime} не поддерживается")

        except Exception as e:
            logger.warning(f"{pair}: ошибка обработки: {e}")

    if not selected:
        logger.warning("Нет выбранных пар! Проверь фильтры в config.json")

    return selected

