# remove_tests_from_root.ps1
# Скрипт удаляет тестовые файлы из корня проекта, если они там остались.
# Все тесты должны находиться в папке tests/, а не в корне.

$files = @(
    "test_logging_setup.py",
    "test_pipeline.py",
    "test_sl_tp.py",
    "test_config.py",
    "test_notifier.py"
)

foreach ($file in $files) {
    $path = Join-Path $PWD $file
    if (Test-Path $path) {
        Remove-Item $path -Force
        Write-Host "? Удалён файл: $file"
    } else {
        Write-Host "? Файл не найден в корне: $file"
    }
}
