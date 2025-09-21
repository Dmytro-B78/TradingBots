import math

def calculate_sl_tp(entry_price: float, side: str, cfg, atr_value: float):
    '''
    Расчёт SL и TP на основе настроек в cfg.sl_tp.
    side: 'long' или 'short'
    atr_value: значение ATR (в тех же единицах, что и цена)
    '''
    sl_type = getattr(cfg.sl_tp, "sl_type", "atr")
    sl_value = getattr(cfg.sl_tp, "sl_value", 2.0)
    tp_type = getattr(cfg.sl_tp, "tp_type", "r_multiple")
    tp_value = getattr(cfg.sl_tp, "tp_value", 3.0)

    # --- Stop Loss ---
    if sl_type == "atr":
        sl_distance = atr_value * sl_value
    elif sl_type == "fixed":
        sl_distance = sl_value
    else:
        raise ValueError(f"Неизвестный sl_type: {sl_type}")

    # --- Take Profit ---
    if tp_type == "r_multiple":
        tp_distance = sl_distance * tp_value
    elif tp_type == "fixed":
        tp_distance = tp_value
    else:
        raise ValueError(f"Неизвестный tp_type: {tp_type}")

    if side.lower() == "long":
        sl_price = entry_price - sl_distance
        tp_price = entry_price + tp_distance
    elif side.lower() == "short":
        sl_price = entry_price + sl_distance
        tp_price = entry_price - tp_distance
    else:
        raise ValueError("side должен быть 'long' или 'short'")

    return {
        "sl_price": round(sl_price, 2),
        "tp_price": round(tp_price, 2),
        "sl_distance": round(sl_distance, 2),
        "tp_distance": round(tp_distance, 2)
    }
