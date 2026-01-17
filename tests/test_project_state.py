# ------------------------------------------------------------------------------------
# FILE: tests/test_project_state.py
# PURPOSE: Отключённый (skip) тест-снэпшот, чтобы не запускать pytest изнутри pytest.
# ------------------------------------------------------------------------------------
import pytest

@pytest.mark.skip(reason="Snapshot выполняется отдельным runner-скриптом (snapshot_runner.py). Исключаем рекурсию и зависания.")
def test_project_state_snapshot():
    assert True

