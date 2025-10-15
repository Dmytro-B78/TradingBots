# ------------------------------------------------------------------------------------
# FILE: snapshot_runner.py
# PURPOSE: Делает snapshot результата pytest и пишет logs/failed_tests.log без рекурсии.
# ------------------------------------------------------------------------------------
import os
import subprocess

SNAPSHOT_FILE = "project_snapshot.txt"
FAILED_FILE = os.path.join("logs", "failed_tests.log")

def main():
    # Гарантируем папку для логов
    os.makedirs("logs", exist_ok=True)

    # Запускаем pytest безопасно, ограничиваем падения и ставим таймаут
    result = subprocess.run(
        ["python", "-m", "pytest", "-q", "--disable-warnings", "--maxfail=5"],
        capture_output=True,
        text=True,
        timeout=300
    )

    # Сохраняем stdout/stderr в snapshot
    with open(SNAPSHOT_FILE, "w", encoding="utf-8") as f:
        f.write(result.stdout)
        if result.stderr:
            f.write("\n--- STDERR ---\n")
            f.write(result.stderr)

    # Парсим упавшие тесты
    lines = result.stdout.splitlines()
    failed = [line for line in lines if "::" in line and "FAILED" in line]

    # Пишем логи падений или удаляем старые
    if failed:
        with open(FAILED_FILE, "w", encoding="utf-8") as f:
            f.write("\n".join(failed))
    elif result.returncode != 0:
        with open(FAILED_FILE, "w", encoding="utf-8") as f:
            f.write("Pytest crashed:\n")
            f.write(result.stderr or "no stderr")
    else:
        if os.path.exists(FAILED_FILE):
            os.remove(FAILED_FILE)

if __name__ == "__main__":
    main()
