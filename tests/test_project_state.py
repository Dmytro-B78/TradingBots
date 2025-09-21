import os
import datetime
import subprocess

SNAPSHOT_FILE = "project_snapshot.txt"
PROJECT_INFO_FILE = "PROJECT_INFO.md"

def test_project_state_snapshot():
    # 1. Дата и время
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 2. Версия проекта из PROJECT_INFO.md
    version = "не найдена"
    if os.path.exists(PROJECT_INFO_FILE):
        with open(PROJECT_INFO_FILE, "r", encoding="utf-8") as f:
            for line in f:
                if "Версия:" in line:
                    parts = line.split("**")
                    if len(parts) >= 3:
                        version = parts[1]
                    else:
                        version = line.strip()
                    break

    # 3. Результат прогона тестов (кроме этого теста)
    try:
        result = subprocess.run(
            [
                "python", "-m", "pytest",
                "--maxfail=1", "--disable-warnings",
                "--ignore=tests/test_project_state.py"
            ],
            capture_output=True, text=True, check=False
        )
        # Объединяем stdout и stderr
        combined_output = result.stdout + "\n" + result.stderr
        # Ищем строку с итогами
        tests_summary = next(
            (line for line in combined_output.splitlines()
             if any(word in line for word in ("passed", "failed", "error"))),
            None
        )
        if not tests_summary:
            tests_summary = "Нет тестов для запуска"
    except Exception as e:
        tests_summary = f"Ошибка запуска тестов: {e}"

    # 4. Последние изменения из PROJECT_INFO.md (раздел 8)
    last_update = "не найдено"
    if os.path.exists(PROJECT_INFO_FILE):
        with open(PROJECT_INFO_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
        in_update_section = False
        for line in lines:
            if "## 8. Обновление" in line:
                in_update_section = True
                continue
            if in_update_section and line.strip().startswith("###"):
                last_update = line.strip()
                break

    # 5. Формируем снимок
    snapshot = (
        f"=== Состояние проекта на {now} ===\n"
        f"Версия проекта: {version}\n"
        f"Последнее обновление: {last_update}\n"
        f"Результат тестов: {tests_summary}\n"
        f"===============================\n"
    )

    # 6. Записываем в файл
    with open(SNAPSHOT_FILE, "w", encoding="utf-8") as f:
        f.write(snapshot)

    # 7. Проверка, что файл создан
    assert os.path.exists(SNAPSHOT_FILE), "Файл project_snapshot.txt не был создан"