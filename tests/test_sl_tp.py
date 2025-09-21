from bot_ai.core.config import load_config
from bot_ai.signals.sl_tp import calculate_sl_tp

def main():
    cfg = load_config("config.json")

    print("\n=== ТЕСТ: SL/TP для LONG ===")
    res_long = calculate_sl_tp(entry_price=100.0, side="long", cfg=cfg, atr_value=2.5)
    print(res_long)

    print("\n=== ТЕСТ: SL/TP для SHORT ===")
    res_short = calculate_sl_tp(entry_price=100.0, side="short", cfg=cfg, atr_value=2.5)
    print(res_short)

if __name__ == "__main__":
    main()
