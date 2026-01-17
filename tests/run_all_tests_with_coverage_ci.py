import os
import shutil
import subprocess
import sys

def main():
    # Чистим старые артефакты
    if os.path.exists(".coverage"):
        os.remove(".coverage")
    if os.path.exists("coverage_reports"):
        shutil.rmtree("coverage_reports")

    os.makedirs("coverage_reports", exist_ok=True)

    # Команда pytest с coverage
    cmd = [
        sys.executable, "-m", "pytest",
        "--maxfail=1", "--disable-warnings", "-q",
        "--cov=bot_ai",
        "--cov-report=json:coverage_reports/coverage.json",
        "--cov-report=csv:coverage_reports/coverage.csv"
    ]

    # Запуск
    result = subprocess.run(cmd)
    if result.returncode != 0:
        sys.exit(result.returncode)

    print("? CI coverage отчёты сохранены в coverage_reports (JSON + CSV)")

if __name__ == "__main__":
    main()

