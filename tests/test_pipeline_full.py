
from bot_ai.selector import pipeline

def test_pipeline_full(monkeypatch, tmp_path):
    """
    Интеграционный тест пайплайна:
    - замокаем whitelist и json.load/json.dump
    - проверим, что select_pairs возвращает непустой список
    """

    # создаём временный whitelist.json
    whitelist_file = tmp_path / "whitelist.json"
    whitelist_file.write_text("[]", encoding="utf-8")

    # мокаем путь к whitelist
    monkeypatch.setattr(
        pipeline,
        "_whitelist_path",
        lambda: str(whitelist_file))

    # мокаем json.load > возвращаем список пар
    monkeypatch.setattr(
        pipeline.json,
        "load",
        lambda f: [
            "AAA/USDT",
            "BBB/USDT"])

    # мокаем json.dump > заглушка
    monkeypatch.setattr(pipeline.json, "dump", lambda obj, f, *a, **k: None)

    # мокаем show_top_pairs > заглушка
    monkeypatch.setattr(
        pipeline,
        "show_top_pairs",
        lambda pairs,
        top_n=2: None)

    # выполняем пайплайн
    cfg = {"volume_threshold": 100}
    result = pipeline.select_pairs(cfg, use_cache=True)

    # проверяем, что список не пустой
    assert result, "select_pairs вернул пустой список"

