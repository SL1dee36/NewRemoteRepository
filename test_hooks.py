"""
Test suite for automated Git Hooks validation.
Runs scenarios to verify pre-commit hook behavior:
1. Rejects commit with unformatted Python code (Black check).
2. Rejects commit with failing tests (unittest).
3. Allows commit with valid code and passing tests.
"""

import os
import subprocess
import sys
from pathlib import Path

# Enable UTF-8 encoding on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

# ANSI colors
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"


def run_cmd(cmd, cwd=None):
    """Executes a command and returns (returncode, stdout, stderr)."""
    result = subprocess.run(
        cmd,
        cwd=cwd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def check_prerequisites(repo_root: Path):
    """Verifies repository, pre-commit hook, and tools."""
    print(f"{CYAN}{BOLD}=== ПРОВЕРКА ПРЕДВАРИТЕЛЬНЫХ ТРЕБОВАНИЙ ==={RESET}")

    hook_path = repo_root / ".git" / "hooks" / "pre-commit"
    if not hook_path.exists():
        print(f"{RED}[ОШИБКА] Хук pre-commit не найден: {hook_path}{RESET}")
        return False
    print(f"{GREEN}[OK] Хук pre-commit обнаружен.{RESET}")

    # Check black
    rc, out, _ = run_cmd("python -m black --version")
    if rc != 0:
        print(f"{RED}[ОШИБКА] Утилита black не установлена!{RESET}")
        return False
    print(f"{GREEN}[OK] Black доступен: {out.splitlines()[0]}{RESET}")
    return True


def test_scenario_1_bad_formatting(repo_root: Path):
    """Scenario 1: Hook must REJECT commit if Black formatting check fails."""
    print(
        f"\n{CYAN}{BOLD}--- ТЕСТ 1: Блокировка при нарушении форматирования (Black) ---{RESET}"
    )

    utils_path = repo_root / "utils.py"
    original_content = utils_path.read_text(encoding="utf-8")

    try:
        bad_code = "\n\ndef _badly_formatted_func(   x,   y  ):\n    return       x+y\n"
        utils_path.write_text(original_content + bad_code, encoding="utf-8")

        run_cmd("git add utils.py", cwd=repo_root)
        rc, out, err = run_cmd(
            'git commit -m "test: commit with bad formatting"', cwd=repo_root
        )

        if rc != 0:
            print(
                f"{GREEN}{BOLD}[ПРОЙДЕН] Хук успешно заблокировал коммит с невалидным форматированием!{RESET}"
            )
            return True
        else:
            print(f"{RED}{BOLD}[ПРОВАЛЕН] Хук пропустил неформатированный код!{RESET}")
            run_cmd("git reset --hard HEAD~1", cwd=repo_root)
            return False
    finally:
        utils_path.write_text(original_content, encoding="utf-8")
        run_cmd("git restore --staged utils.py", cwd=repo_root)
        run_cmd("git checkout utils.py", cwd=repo_root)


def test_scenario_2_failing_tests(repo_root: Path):
    """Scenario 2: Hook must REJECT commit if unit tests fail."""
    print(
        f"\n{CYAN}{BOLD}--- ТЕСТ 2: Блокировка при непройденных тестах (unittest) ---{RESET}"
    )

    test_path = repo_root / "test_app.py"
    original_content = test_path.read_text(encoding="utf-8")

    try:
        broken_test = "\n    def test_hook_intentional_failure(self):\n        self.assertEqual(2 * 2, 999, 'Intentional test failure for hook')\n"
        if 'if __name__ == "__main__":' in original_content:
            parts = original_content.split('if __name__ == "__main__":')
            new_content = (
                parts[0] + broken_test + '\nif __name__ == "__main__":' + parts[1]
            )
        else:
            new_content = original_content + broken_test

        test_path.write_text(new_content, encoding="utf-8")
        run_cmd("python -m black test_app.py", cwd=repo_root)

        run_cmd("git add test_app.py", cwd=repo_root)
        rc, out, err = run_cmd(
            'git commit -m "test: commit with failing test"', cwd=repo_root
        )

        if rc != 0:
            print(
                f"{GREEN}{BOLD}[ПРОЙДЕН] Хук успешно заблокировал коммит с падающим тестом!{RESET}"
            )
            return True
        else:
            print(
                f"{RED}{BOLD}[ПРОВАЛЕН] Хук пропустил коммит с падающим тестом!{RESET}"
            )
            run_cmd("git reset --hard HEAD~1", cwd=repo_root)
            return False
    finally:
        test_path.write_text(original_content, encoding="utf-8")
        run_cmd("git restore --staged test_app.py", cwd=repo_root)
        run_cmd("git checkout test_app.py", cwd=repo_root)


def test_scenario_3_valid_commit(repo_root: Path):
    """Scenario 3: Hook must ALLOW commit if formatting and tests pass."""
    print(
        f"\n{CYAN}{BOLD}--- ТЕСТ 3: Разрешение коммита при корректном коде и тестах ---{RESET}"
    )

    utils_path = repo_root / "utils.py"
    original_utils = utils_path.read_text(encoding="utf-8")

    test_path = repo_root / "test_app.py"
    original_tests = test_path.read_text(encoding="utf-8")

    try:
        valid_func = '\n\ndef is_positive(number: float) -> bool:\n    """Checks if number is greater than zero."""\n    return number > 0\n'
        utils_path.write_text(original_utils + valid_func, encoding="utf-8")

        passing_test = "\n    def test_is_positive(self):\n        from utils import is_positive\n        self.assertTrue(is_positive(5))\n        self.assertFalse(is_positive(-5))\n"
        parts = original_tests.split('if __name__ == "__main__":')
        new_tests = parts[0] + passing_test + '\nif __name__ == "__main__":' + parts[1]
        test_path.write_text(new_tests, encoding="utf-8")

        run_cmd("python -m black utils.py test_app.py", cwd=repo_root)

        run_cmd("git add utils.py test_app.py", cwd=repo_root)
        rc, out, err = run_cmd(
            'git commit -m "test(hook): valid addition of is_positive"',
            cwd=repo_root,
        )

        if rc == 0:
            print(
                f"{GREEN}{BOLD}[ПРОЙДЕН] Хук успешно разрешил коммит валидного кода!{RESET}"
            )
            run_cmd("git reset --hard HEAD~1", cwd=repo_root)
            return True
        else:
            print(
                f"{RED}{BOLD}[ПРОВАЛЕН] Хук ошибочно заблокировал валидный коммит!{RESET}"
            )
            return False
    finally:
        utils_path.write_text(original_utils, encoding="utf-8")
        test_path.write_text(original_tests, encoding="utf-8")
        run_cmd("git restore --staged utils.py test_app.py", cwd=repo_root)
        run_cmd("git checkout utils.py test_app.py", cwd=repo_root)


def main():
    repo_root = Path(__file__).resolve().parent
    print(
        f"{BOLD}Запуск автоматического тестирования Git-хуков в: {repo_root}{RESET}\n"
    )

    if not check_prerequisites(repo_root):
        sys.exit(1)

    results = []
    results.append(
        (
            "1. Блокировка нарушения Black",
            test_scenario_1_bad_formatting(repo_root),
        )
    )
    results.append(
        ("2. Блокировка падающих тестов", test_scenario_2_failing_tests(repo_root))
    )
    results.append(
        (
            "3. Разрешение валидного коммита",
            test_scenario_3_valid_commit(repo_root),
        )
    )

    print(f"\n{CYAN}{BOLD}==========================================")
    print("ИТОГОВЫЙ ОТЧЕТ ТЕСТИРОВАНИЯ ХУКОВ")
    print(f"=========================================={RESET}")

    all_passed = True
    for name, passed in results:
        status = f"{GREEN}[ПРОЙДЕН]{RESET}" if passed else f"{RED}[ПРОВАЛЕН]{RESET}"
        print(f"{status} {name}")
        if not passed:
            all_passed = False

    print("------------------------------------------")
    if all_passed:
        print(f"{GREEN}{BOLD} Все проверки Git-хука успешно пройдены!{RESET}\n")
        sys.exit(0)
    else:
        print(f"{RED}{BOLD} Часть тестов завершилась ошибкой.{RESET}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
