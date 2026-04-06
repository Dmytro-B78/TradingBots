import sys, csv
sys.path.append('C:/TradingBots/NT')

from bot_ai.strategy.meta_strategy import MetaStrategy

path = 'C:/TradingBots/candles/compiled/SOLUSDT-1m.csv'
print('Using:', path)

candles = []
with open(path, 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        if len(row) < 6:
            continue
        candles.append({
            'open': float(row[1]),
            'high': float(row[2]),
            'low': float(row[3]),
            'close': float(row[4]),
            'volume': float(row[5])
        })

print('Loaded:', len(candles))

ms = MetaStrategy({})

# прогреваем стратегию
for c in candles[:-500]:
    ms.on_candle(c)

# выводим последние 200 свечей
for i, c in enumerate(candles[-200:]):
    decision = ms.on_candle(c)
    print(i, c['close'], ms.regime, (decision or {}).get('signal'))
