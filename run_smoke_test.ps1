# Запуск smoke-теста с подробным выводом
# Убедись, что ты находишься в корне проекта (где лежит tests/)
python -m pytest tests/test_smoke.py -v --tb=short --maxfail=1
