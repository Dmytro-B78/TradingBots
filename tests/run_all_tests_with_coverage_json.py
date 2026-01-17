import os
import shutil
import subprocess
import sys

def main():
    # Чистим старые артефакты
    if os.path.exists(".coverage"):
        os.remove(".coverage")
    for folder in ["htmlcov", "coverage_reports"]:
        if os.path.exists(folder):
            shutil.rmtree(folder)

    os.makedirs("coverage_reports", exist_ok=True)

    # Команда pytest с coverage
    cmd = [
        sys.executable, "-m", "pytest",
        "--maxfail=1", "--disable-warnings", "-q",
        "--cov=bot_ai",
        "--cov-report=term-missing",
        "--cov-report=html",
        "--cov-report=json:coverage_reports/coverage.json",
        "--cov-report=csv:coverage_reports/coverage.csv"
    ]

    # Запуск
    result = subprocess.run(cmd)
    if result.returncode != 0:
        sys.exit(result.returncode)

    # Автооткрытие HTML-отчёта
    index_path = os.path.join("htmlcov", "index.html")
    if os.path.exists(index_path):
        if sys.platform.startswith("win"):
            os.startfile(index_path)  # Windows
        elif sys.platform == "darwin":
            subprocess.run(["open", index_path])  # macOS
        else:
            subprocess.run(["xdg-open", index_path])  # Linux

    print("? Coverage отчёты сохранены в папке coverage_reports")

if __name__ == "__main__":
    main()

