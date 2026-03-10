# bot_ai/selector/pipeline_utils.py
# Utility functions for pipeline operations

def _safe_ticker(symbol: str) -> str:
    return symbol.replace("/", "").replace("-", "").upper()

def _cache_valid(cache: dict, key: str, ttl: int) -> bool:
    if key not in cache:
        return False
    timestamp, _ = cache[key]
    from time import time
    return (time() - timestamp) < ttl

def _get_exchange_name(cfg):
    return cfg.exchange.lower()

def get_data(symbol, interval, lookback, source, **kwargs):
    """Placeholder for fetching OHLCV data for a symbol."""
    raise NotImplementedError("get_data must be implemented or mocked in tests")

def log_signal(signal, **kwargs):
    """Placeholder for logging strategy signals."""
    pass
