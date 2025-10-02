# remove_tests_from_root.ps1
# ������ ������� �������� ����� �� ����� �������, ���� ��� ��� ��������.
# ��� ����� ������ ���������� � ����� tests/, � �� � �����.

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
        Write-Host "? ����� ����: $file"
    } else {
        Write-Host "? ���� �� ������ � �����: $file"
    }
}
