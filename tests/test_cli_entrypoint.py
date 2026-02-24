# tests/test_cli_entrypoint.py — проверка запуска main.py

import importlib.util
import pathlib
import pytest

def test_cli_entrypoint_runs():
    script_path = pathlib.Path(__file__).parent.parent / "main.py"
    if not script_path.exists():
        pytest.skip("main.py не найден")

    spec = importlib.util.spec_from_file_location("main", script_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    assert hasattr(module, "main"), "main.py должен содержать функцию main()"
    module.main()

