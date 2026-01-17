import json
import os
from types import SimpleNamespace

def dict_to_namespace(d):
    """
    Рекурсивно превращает словарь в объект SimpleNamespace
    для доступа к полям через точку.
    """
    if isinstance(d, dict):
        return SimpleNamespace(**{k: dict_to_namespace(v)
                               for k, v in d.items()})
    elif isinstance(d, list):
        return [dict_to_namespace(i) for i in d]
    else:
        return d

def load_config(path='config.json'):
    """
    Загружает конфигурацию из JSON-файла и возвращает объект с доступом через точку.
    Поддерживает файлы с BOM (utf-8-sig) и заполняет отсутствующие секции значениями по умолчанию.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Config file '{path}' not found")

    # Читаем с поддержкой BOM
    with open(path, 'r', encoding='utf-8-sig') as f:
        data = json.load(f)

    # Значения по умолчанию для новых секций
    defaults = {
        "risk": {
            "min_24h_volume_usdt": 1000000,
            "max_spread_pct": 0.5,
            "max_daily_loss_pct": 5,
            "max_positions": 3,
            "max_position_size_pct": 20,
            "kill_switch_loss_pct": 10
        },
        "sl_tp": {
            "sl_type": "atr",
            "sl_value": 2.0,
            "tp_type": "r_multiple",
            "tp_value": 3.0
        },
        "pair_selection": {
            "d1_timeframe": "1d",
            "d1_sma_fast": 50,
            "d1_sma_slow": 200,
            "ltf_timeframe": "1h",
            "ltf_sma_fast": 20,
            "ltf_sma_slow": 50
        }
    }

    # Заполняем отсутствующие ключи значениями по умолчанию
    for section, params in defaults.items():
        if section not in data:
            data[section] = params
        else:
            for key, val in params.items():
                if key not in data[section]:
                    data[section][key] = val

    return dict_to_namespace(data)

