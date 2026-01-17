# scripts/generate_test_report.py
# ------------------------------------------------------------
# Назначение:
# 1. Запустить тесты через python -m pytest (без зависимости от PATH)
# 2. Сгенерировать HTML-отчёт покрытия кода
# 3. Записать результаты тестов в changes.log с отметкой времени
# ------------------------------------------------------------

import datetime
import subprocess

def main():
    # Получаем текущее время для лога
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Запуск pytest через python -m pytest
    result = subprocess.run(["python",
                             "-m",
                             "pytest",
                             "--maxfail=1",
                             "--disable-warnings",
                             "--cov=bot_ai",
                             "--cov-report=html"],
                            capture_output=True,
                            text=True)

    # Формируем запись для changes.log
    log_entry = f"{timestamp} — Тесты выполнены\\n{result.stdout}\\n"
    with open("changes.log", "a", encoding="utf-8") as log_file:
        log_file.write(log_entry)

    print("Отчёт по тестам сохранён в htmlcov/, лог обновлён.")

if __name__ == "__main__":
    main()

