import json
import pytest

def test_config_loader_all_branches(tmp_path):
    from bot_ai.core.config_loader import Config

    # 1. Проверка: файл не существует → FileNotFoundError
    with pytest.raises(FileNotFoundError):
        Config.load(tmp_path / "no_config.json")

    # 2. Проверка: корректная загрузка JSON
    config_file = tmp_path / "config.json"
    data = {"key1": "value1", "nested": {"key2": "value2"}}
    config_file.write_text(json.dumps(data), encoding="utf-8")

    cfg = Config.load(config_file)
    assert isinstance(cfg, Config)
    assert cfg["key1"] == "value1"
    assert cfg["nested"]["key2"] == "value2"
    assert "key1" in cfg
    assert "nested" in cfg
