import os

def test_no_header_in_middle():
    log_path = os.path.join("data", "trades_log.csv")
    assert os.path.exists(log_path), f"Файл {log_path} не найден"

    with open(log_path, "r", encoding="utf-8-sig") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) > 2, "В логе должно быть минимум 2 строки сделок + заголовок"

    header = lines[0]
    # Проверяем, что заголовок встречается только в первой строке
    for i, line in enumerate(lines[1:], start=2):
        assert line != header, f"Повтор заголовка найден в строке {i}: {line}"

    print("✅ Заголовок в середине файла не найден — всё ок")
