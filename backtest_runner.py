# backtest_runner.py
# Р вЂ”Р В°Р С—РЎС“РЎРѓР С” Р В±РЎРЊР С”РЎвЂљР ВµРЎРѓРЎвЂљР В° РЎРѓРЎвЂљРЎР‚Р В°РЎвЂљР ВµР С–Р С‘Р С‘

from bot_ai.backtest.simulator import simulate

simulate(
    pair="BTCUSDT",
    timeframe="1h",
    strategy="volume_spike",
    rsi_threshold=65,
    capital=10000,
    risk_pct=1.0
)

