from types import SimpleNamespace

import pandas as pd

from bot_ai.exec.executor import TradeExecutor

def main():
    # Р¤РµР№РєРѕРІР°СЏ РєРѕРЅС„РёРіСѓСЂР°С†РёСЏ
    cfg = SimpleNamespace()
    cfg.mode = "dry-run"
    cfg.risk = SimpleNamespace(test_equity=1000)

    # вњ… Р”РѕР±Р°РІР»СЏРµРј С„РµР№РєРѕРІСѓСЋ СЃРµРєС†РёСЋ sl_tp, С‡С‚РѕР±С‹ РЅРµ РїР°РґР°Р» СЂР°СЃС‡С‘С‚ SL/TP
    cfg.sl_tp = SimpleNamespace(
        atr_multiplier_sl=1.0,
        atr_multiplier_tp=2.0
    )

    # Р¤РµР№РєРѕРІС‹Рµ РґР°РЅРЅС‹Рµ OHLCV
    ohlcv_df = pd.DataFrame({
        "high": [120, 121, 122],
        "low": [100, 101, 102],
        "close": [110, 111, 112]
    })

    # РЎРѕР·РґР°С‘Рј РёСЃРїРѕР»РЅРёС‚РµР»СЏ СЃРґРµР»РѕРє
    executor = TradeExecutor(cfg)

    # РћС‚РєСЂС‹РІР°РµРј СЃРґРµР»РєСѓ СЃ РєРѕРјРјРµРЅС‚Р°СЂРёРµРј
    executor.execute_trade(
        "BTC/USDT",
        "buy",
        110.0,
        ohlcv_df,
        comment="РЎРёРіРЅР°Р» РїРѕ EMA crossover"
    )

    print("РЎРґРµР»РєР° РІС‹РїРѕР»РЅРµРЅР°. РџСЂРѕРІРµСЂСЊС‚Рµ С„Р°Р№Р» data/trades_log.csv")

if __name__ == "__main__":
    main()

