import os
import shutil
import subprocess
import sys

def main():
    # Чистим старые артефакты
    if os.path.exists(".coverage"):
        os.remove(".coverage")
    if os.path.exists("htmlcov"):
        shutil.rmtree("htmlcov")

    # Команда pytest с coverage
    cmd = [
        sys.executable, "-m", "pytest",
        "--maxfail=1", "--disable-warnings", "-q",
        "--cov=bot_ai",
        "--cov-report=term-missing",
        "--cov-report=html"
    ]

    # Запуск
    result = subprocess.run(cmd)
    if result.returncode != 0:
        sys.exit(result.returncode)

    # Автооткрытие отчёта
    index_path = os.path.join("htmlcov", "index.html")
    if os.path.exists(index_path):
        if sys.platform.startswith("win"):
            os.startfile(index_path)  # Windows
        elif sys.platform == "darwin":
            subprocess.run(["open", index_path])  # macOS
        else:
            subprocess.run(["xdg-open", index_path])  # Linux

if __name__ == "__main__":
    main()

