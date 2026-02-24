import os

# Проверяет, что файл trades_log.csv существует и не содержит повторяющихся заголовков в середине
def test_no_header_in_middle():
    log_path = os.path.join("st", "trades_log.csv")
    assert os.path.exists(log_path), f"Файл {log_path} не найден"

    with open(log_path, encoding="utf-8") as f:
        lines = f.readlines()

    header = lines[0].strip()
    for i, line in enumerate(lines[1:], start=2):
        assert line.strip() != header, f"Повтор заголовка на строке {i}: {line.strip()}"
