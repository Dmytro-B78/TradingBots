# remove_root_tests.ps1
# Удаляет все файлы test_*.py из корня проекта, кроме папки tests/

# Получаем список всех файлов в корне, начинающихся на test_ и с расширением .py
Get-ChildItem -Path $PWD -Filter "test_*.py" -File | ForEach-Object {
    $fullPath = $_.FullName
    # Проверяем, что файл не находится в папке tests
    if ($fullPath -notmatch "\\tests\\") {
        Remove-Item $fullPath -Force
        Write-Host "? Удалён файл: $($_.Name)"
    }
}
