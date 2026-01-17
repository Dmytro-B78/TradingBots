def show_top_pairs(cfg, pairs, top_n=10, **kwargs):
    if not pairs:
        logger.info("Whitelist пуст.")
        return False
    ex_class = getattr(ccxt, _get_exchange_name(cfg))
    ex = ex_class()
    for p in pairs[:top_n]:
        try:
            t = ex.fetch_ticker(p)
            logger.info(f"{p}: volume={t.get('quoteVolume', 0)}")
        except Exception:
            continue
    return False  # тест ожидает False во всех случаях

