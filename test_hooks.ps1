<#
.SYNOPSIS
Скрипт автоматического тестирования Git-хуков (pre-commit).

.DESCRIPTION
Скрипт проверяет работу хука .git/hooks/pre-commit по 3 сценариям:
1. Попытка коммита неотформатированного кода (должен быть отклонен Black).
2. Попытка коммита с падающим unit-тестом (должен быть отклонен unittest).
3. Попытка коммита валидного кода (должен успешно пройти).
#>

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$Host.UI.RawUI.ForegroundColor = "White"

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "  АВТОМАТИЗИРОВАННОЕ ТЕСТИРОВАНИЕ GIT-ХУКОВ (PRE-COMMIT)" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

$repoRoot = (Get-Item -Path ".").FullName
$hookPath = Join-Path $repoRoot ".git\hooks\pre-commit"

if (-not (Test-Path $hookPath)) {
    Write-Host "[ОШИБКА] Хук pre-commit не найден по пути: $hookPath" -ForegroundColor Red
    exit 1
}
Write-Host "[OK] Хук pre-commit обнаружен." -ForegroundColor Green

# Проверка наличия black
try {
    $blackVersion = python -m black --version 2>&1
    Write-Host "[OK] Black доступен: $blackVersion" -ForegroundColor Green
} catch {
    Write-Host "[ОШИБКА] Black не найден в Python!" -ForegroundColor Red
    exit 1
}

$results = @()

# -------------------------------------------------------------
# ТЕСТ 1: Блокировка коммита при нарушении форматирования Black
# -------------------------------------------------------------
Write-Host "`n--- ТЕСТ 1: Проверка блокировки при нарушении стиля Black ---" -ForegroundColor Yellow
$utilsOriginal = Get-Content utils.py -Raw -Encoding utf8
try {
    Add-Content -Path utils.py -Value "`n`ndef bad_style_function(   x,   y   ):`n    return      x+y`n" -Encoding utf8
    git add utils.py
    $commitOutput = git commit -m "test: commit with bad style" 2>&1
    $exitCode = $LASTEXITCODE

    if ($exitCode -ne 0) {
        Write-Host "[ПРОЙДЕН] Хук успешно заблокировал коммит с невалидным форматированием!" -ForegroundColor Green
        $results += [PSCustomObject]@{ Test = "1. Блокировка нарушения Black"; Result = "ПРОЙДЕН" }
    } else {
        Write-Host "[ПРОВАЛЕН] Хук пропустил неформатированный код!" -ForegroundColor Red
        git reset --hard HEAD~1 | Out-Null
        $results += [PSCustomObject]@{ Test = "1. Блокировка нарушения Black"; Result = "ПРОВАЛЕН" }
    }
} finally {
    Set-Content -Path utils.py -Value $utilsOriginal -Encoding utf8
    git restore --staged utils.py 2>$null
    git checkout utils.py 2>$null
}

# -------------------------------------------------------------
# ТЕСТ 2: Блокировка коммита при упавшем тесте
# -------------------------------------------------------------
Write-Host "`n--- ТЕСТ 2: Проверка блокировки при непройденном тесте ---" -ForegroundColor Yellow
$testsOriginal = Get-Content test_app.py -Raw -Encoding utf8
try {
    $failingTest = "`n    def test_hook_failure_verification(self):`n        self.assertEqual(2 + 2, 999, 'Test failure for hook')`n"
    if ($testsOriginal.Contains('if __name__ == "__main__":')) {
        $parts = $testsOriginal.Split('if __name__ == "__main__":')
        $newTests = $parts[0] + $failingTest + "`nif __name__ == `"__main__`":" + $parts[1]
    } else {
        $newTests = $testsOriginal + $failingTest
    }
    Set-Content -Path test_app.py -Value $newTests -Encoding utf8
    python -m black test_app.py | Out-Null

    git add test_app.py
    $commitOutput = git commit -m "test: commit with failing test" 2>&1
    $exitCode = $LASTEXITCODE

    if ($exitCode -ne 0) {
        Write-Host "[ПРОЙДЕН] Хук успешно заблокировал коммит с падающим тестом!" -ForegroundColor Green
        $results += [PSCustomObject]@{ Test = "2. Блокировка падающих тестов"; Result = "ПРОЙДЕН" }
    } else {
        Write-Host "[ПРОВАЛЕН] Хук пропустил коммит с падающим тестом!" -ForegroundColor Red
        git reset --hard HEAD~1 | Out-Null
        $results += [PSCustomObject]@{ Test = "2. Блокировка падающих тестов"; Result = "ПРОВАЛЕН" }
    }
} finally {
    Set-Content -Path test_app.py -Value $testsOriginal -Encoding utf8
    git restore --staged test_app.py 2>$null
    git checkout test_app.py 2>$null
}

# -------------------------------------------------------------
# ТЕСТ 3: Успешный коммит при корректном коде
# -------------------------------------------------------------
Write-Host "`n--- ТЕСТ 3: Проверка разрешения корректного коммита ---" -ForegroundColor Yellow
try {
    $validFunc = "`n`ndef square_number(n: float) -> float:`n    `"`"`"Returns square of number.`"`"`"`n    return n * n`n"
    Add-Content -Path utils.py -Value $validFunc -Encoding utf8

    $validTest = "`n    def test_square_number(self):`n        from utils import square_number`n        self.assertEqual(square_number(4), 16)`n"
    $currentTests = Get-Content test_app.py -Raw -Encoding utf8
    $parts = $currentTests.Split('if __name__ == "__main__":')
    $newTests = $parts[0] + $validTest + "`nif __name__ == `"__main__`":" + $parts[1]
    Set-Content -Path test_app.py -Value $newTests -Encoding utf8

    python -m black utils.py test_app.py | Out-Null

    git add utils.py test_app.py
    $commitOutput = git commit -m "test(hook): valid addition of square_number" 2>&1
    $exitCode = $LASTEXITCODE

    if ($exitCode -eq 0) {
        Write-Host "[ПРОЙДЕН] Хук успешно разрешил коммит валидного кода!" -ForegroundColor Green
        $results += [PSCustomObject]@{ Test = "3. Разрешение валидного коммита"; Result = "ПРОЙДЕН" }
        git reset --hard HEAD~1 | Out-Null
    } else {
        Write-Host "[ПРОВАЛЕН] Хук ошибочно заблокировал валидный коммит!" -ForegroundColor Red
        $results += [PSCustomObject]@{ Test = "3. Разрешение валидного коммита"; Result = "ПРОВАЛЕН" }
    }
} finally {
    Set-Content -Path utils.py -Value $utilsOriginal -Encoding utf8
    Set-Content -Path test_app.py -Value $testsOriginal -Encoding utf8
    git restore --staged utils.py test_app.py 2>$null
    git checkout utils.py test_app.py 2>$null
}

# -------------------------------------------------------------
# ИТОГОВЫЙ ОТЧЕТ
# -------------------------------------------------------------
Write-Host "`n==========================================================" -ForegroundColor Cyan
Write-Host "                ИТОГОВЫЙ РЕЗУЛЬТАТ ТЕСТОВ                 " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan
$results | Format-Table -AutoSize

$failed = $results | Where-Object { $_.Result -eq "ПРОВАЛЕН" }
if ($failed.Count -eq 0) {
    Write-Host " Все проверки Git-хука успешно пройдены!" -ForegroundColor Green
    exit 0
} else {
    Write-Host " Некоторые тесты хука завершились неудачей." -ForegroundColor Red
    exit 1
}
