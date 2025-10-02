# remove_root_tests.ps1
# ������� ��� ����� test_*.py �� ����� �������, ����� ����� tests/

# �������� ������ ���� ������ � �����, ������������ �� test_ � � ����������� .py
Get-ChildItem -Path $PWD -Filter "test_*.py" -File | ForEach-Object {
    $fullPath = $_.FullName
    # ���������, ��� ���� �� ��������� � ����� tests
    if ($fullPath -notmatch "\\tests\\") {
        Remove-Item $fullPath -Force
        Write-Host "? ����� ����: $($_.Name)"
    }
}
