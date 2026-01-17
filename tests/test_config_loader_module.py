import json

import pytest

def test_config_loader_all_branches(tmp_path):
    from bot_ai.core.config_loader import Config

    # 1. Файл отсутствует > FileNotFoundError
    with pytest.raises(FileNotFoundError):
        Config.load(tmp_path / "no_config.json")

    # 2. Файл существует > загрузка
    config_file = tmp_path / "config.json"
    data = {"key1": "value1", "nested": {"key2": "value2"}}
    config_file.write_text(json.dumps(data), encoding="utf-8")

    cfg = Config.load(config_file)
    assert isinstance(cfg, Config)
    assert cfg["key1"] == "value1"
    assert "key1" in cfg

    # 3. Метод get — существующий ключ
    assert cfg.get("key1") == "value1"

    # 4. Метод get — вложенный ключ
    assert cfg.get("nested", "key2") == "value2"

    # 5. Метод get — отсутствующий ключ > default
    assert cfg.get("missing", default="de") == "def"

    # 6. Метод get — ключ не строка > TypeError
    with pytest.raises(TypeError):
        cfg.get(123)

    # 7. __repr__ содержит ключи
    assert "key1" in repr(cfg)

