import json
from types import SimpleNamespace

def load_config(path='config.json'):
    # utf-8-sig автоматически уберёт BOM, если он есть
    with open(path, 'r', encoding='utf-8-sig') as f:
        data = json.load(f)
    # Преобразуем словарь в объект с доступом через точку
    return json.loads(json.dumps(data), object_hook=lambda d: SimpleNamespace(**d))
