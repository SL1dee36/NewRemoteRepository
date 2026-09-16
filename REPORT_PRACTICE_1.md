# Отчет по практической работе № 1
## Тема: «Система контроля версий Git» + Вариант 4 «Использование хуков для автоматизации процессов»

**Студент:** Nazaryan ART  
**GitHub аккаунт:** [SL1dee36](https://github.com/SL1dee36)  
**Удаленный репозиторий (Remote):** [https://github.com/SL1dee36/NewRemoteRepository](https://github.com/SL1dee36/NewRemoteRepository)  

---

## 1. Краткое резюме выполненных работ

В ходе выполнения практической работы были смоделированы все ключевые аспекты профессиональной командной разработки с использованием распределенной системы контроля версий Git:
1. Создание удаленного репозитория на GitHub с описанием и первичное клонирование.
2. Организация рабочих копий для 3-х разработчиков (`person1`, `person2`, `person3`) с индивидуальными профилями.
3. Разработка модульного Python-приложения из 3-х исходных файлов (`app.py`, `utils.py`, `test_app.py`).
4. Обмен коммитами между разработчиками через `git push` и `git pull`.
5. Создание и публикация функциональных веток (`dev`, `dev1`, `dev2`, `dev3`).
6. Использование `git commit --amend` для корректировки коммитов.
7. Сравнительное исследование трех стратегий слияния: **Merge (`--no-ff`)**, **Squash (`--squash`)**, **Rebase**.
8. Создание реальной ситуации **конфликта слияния (Merge Conflict)** при одновременной правке файла `utils.py` несколькими разработчиками, исследование маркеров конфликта и его разрешение.
9. Применение продвинутых команд: `git log -p`, `git reset --hard`, `git cherry-pick`, `git rebase` и интерактивный `git rebase -i`.
10. Генерация патчей (`git format-patch`) и их применение (`git apply`).
11. **Вариант 4:** Реализация pre-commit хука (`.git/hooks/pre-commit`) для автоматической валидации форматирования кода через `black` и прогона unit-тестов перед каждым коммитом.

---

## 2. Пошаговый отчет о выполнении

### Шаг 1. Создание приложения и первый коммит (Разработчик `person1`)
- Склонирован удаленный репозиторий в каталог `person1`.
- Создано приложение на Python:
  - `app.py` — точка входа в приложение (консольный интерфейс);
  - `utils.py` — математические функции (`add`, `multiply`, `format_result`);
  - `test_app.py` — модульные тесты (`unittest`).
- Зафиксирован коммит и отправлен в Remote:
  ```bash
  git add app.py utils.py test_app.py
  git commit -m "feat(app): add initial MathApp with 3 files (app.py, utils.py, test_app.py)"
  git push origin main
  ```
  *Хэш коммита в GitHub:* `421203b`

---

### Шаг 2. Клонирование `person2`, внесение изменений и синхронизация
- Клонирован репозиторий во вторую рабочую директорию:
  ```bash
  git clone <url> person2
  ```
- В `person2/utils.py` добавлена функция `subtract`:
  ```python
  def subtract(a: float, b: float) -> float:
      """Returns the difference of two numbers."""
      return a - b
  ```
- Выполнен коммит и push из `person2`:
  ```bash
  git commit -am "feat(utils): add subtract function"
  git push origin main
  ```
  *Хэш коммита:* `a97736b`
- В директории `person1` выполнена проверка отсутствия изменений, после чего скачано обновление:
  ```bash
  git pull origin main
  ```
- В `person1` доработан файл `app.py` (вызов `subtract`) и дополнены тесты в `test_app.py`, сделан коммит `4e8d425` и отправлен в Remote. В `person2` выполнен `git pull` для синхронизации.

---

### Шаг 3. Создание функциональных веток `dev` и `dev2`, использование `--amend`
1. **В `person1`:**
   ```bash
   git checkout -b dev
   # Создан файл config.py
   git add config.py
   git commit -m "feat(config): add configuration module in dev branch"
   git push -u origin dev
   ```
   *Хэш:* `a9a70bb`
2. **В `person2`:**
   ```bash
   git fetch origin
   git checkout -b dev2
   # Создан файл logger.py
   git add logger.py
   git commit -m "feat(logger): add basic action logging"
   git push -u origin dev2
   # Доработан logger.py (добавлены уровни логирования), изменения объединены с прошлым коммитом:
   git add logger.py
   git commit --amend -m "feat(logger): add action logging with log levels (amended)"
   git push --force origin dev2
   ```
   *Хэш до amend:* `f496225` -> *Хэш после amend:* `7267082`

---

### Шаг 4. Исследование методов слияния: Merge, Squash, Rebase

| Метод слияния | Описание механизма | Влияние на граф истории | Когда использовать |
| :--- | :--- | :--- | :--- |
| **Merge (`git merge --no-ff`)** | Создает специальный *Merge Commit*, имеющий двух родителей. Сохраняет историю ветвления и все индивидуальные коммиты. | Нелинейная история с явными «петлями» ветвления. | Слияние крупных релизных или долгоживущих веток, где важен контекст разработки. |
| **Squash (`git merge --squash`)** | «Схлопывает» все коммиты из ветки фичи в одно общее изменение в рабочей директории целевой ветки. | Полностью линейная история, история ветви не сохраняется. | Вливание небольших задач с множеством промежуточных («грязных») коммитов (wip, fix typo). |
| **Rebase (`git rebase`)** | Переносит базовый коммит ветки фичи на верхушку целевой ветки, последовательно переприменяя коммиты. | Идеально плоская, линейная история без merge-коммитов. | Подтягивание свежих изменений из `main` в свою ветку перед созданием Pull Request. |

#### Результаты тестов слияния:
- **Граф `git merge --no-ff`**:
  ```text
  *   01b85e1 Merge branch 'feature-merge' into test-merge-base
  |\  
  | * 4564216 feat(merge): part B
  | * 7b3dcdd feat(merge): part A
  |/  
  * 4e8d425 feat(app): use subtract in main application
  ```
- **Граф `git merge --squash`**:
  ```text
  * 01dad7d feat(squash): squashed feature-squash into single commit
  * 4e8d425 feat(app): use subtract in main application
  ```
- **Граф `git rebase`**:
  ```text
  * 343215e feat(rebase): add feature rebase commit
  * 83f8d0f chore: base update before rebase
  * 4e8d425 feat(app): use subtract in main application
  ```

---

### Шаг 5. Симуляция работы 3-х разработчиков и разрешение конфликта слияния

1. **Разработчик `person3`**:
   - Создает ветку `dev3` и модифицирует заголовки и функцию `add` в `utils.py`:
     ```python
     def add(a: float, b: float) -> float:
         """Returns the sum of two numbers (Person 3 implementation)."""
         return float(a + b)
     ```
   - Коммит `86e7a18`, пуш в `origin/dev3`.
2. **Разработчик `person2`**:
   - В ветке `dev2` модифицирует другой файл (`app.py`), добавляя логирование:
   - Коммит `e29fb56`, пуш в `origin/dev2`.
3. **Разработчик `person1`**:
   - В ветке `dev1` модифицирует **тот же файл и ту же функцию `add`** в `utils.py`:
     ```python
     def add(a: float, b: float) -> float:
         """Returns the sum of two numbers with 4-decimal rounding (Person 1 implementation)."""
         return round(a + b, 4)
     ```
   - Коммит `28b31c2`, пуш в `origin/dev1`.

#### Процесс поочередного слияния в `main`:
1. `git merge origin/dev3` -> Успешно (Fast-Forward).
2. `git merge origin/dev2` -> Успешно (автоматическое слияние ort, разные файлы).
3. `git merge dev1` -> **КОНФЛИКТ СЛИЯНИЯ**:
   ```text
   Auto-merging utils.py
   CONFLICT (content): Merge conflict in utils.py
   Automatic merge failed; fix conflicts and then commit the result.
   ```

#### Маркеры конфликта в `utils.py`:
```python
<<<<<<< HEAD
"""Math utility functions - Enterprise Edition by Person 3."""

def add(a: float, b: float) -> float:
    """Returns the sum of two numbers (Person 3 implementation)."""
    return float(a + b)
=======
"""Math utility functions - High Precision Edition by Person 1."""

def add(a: float, b: float) -> float:
    """Returns the sum of two numbers with 4-decimal rounding (Person 1 implementation)."""
    return round(a + b, 4)
>>>>>>> dev1
```

#### Разрешение конфликта:
Конфликт разрешен объединением требований обоих разработчиков (приведение к `float` и округление `round`):
```python
"""Math utility functions - Enterprise High Precision Edition (Merged Person 1 & Person 3)."""

def add(a: float, b: float) -> float:
    """Returns the sum of two numbers with rounding and float conversion."""
    return round(float(a + b), 4)
```
После разрешения:
```bash
git add utils.py
git commit -m "Merge branch 'dev1' into main: resolve conflict in utils.py"
git push origin main
```
*Хэш merge-коммита:* `862d2af`

---

### Шаг 6. Продвинутые команды Git

1. **`git log -p`**:
   Просмотр подробных диффов и патчей для каждого коммита в истории.
2. **`git reset --hard <commit_hash>`**:
   Откат рабочей директории и указателя HEAD до состояния коммита `86e7a18` с безвозвратным удалением несохраненных изменений в рабочей ветке.
3. **`git cherry-pick <commit_hash>`**:
   Выборочный перенос коммита добавления `logger.py` (`7267082`) из ветки `dev2` в изолированную ветку без слияния всей ветки `dev2`.
4. **`git rebase`**:
   Перебазирование ветки `dev1` на актуальную ветку `origin/dev`: коммит `28b31c2` был перенесен поверх коммита `a9a70bb`.
5. **Интерактивный `git rebase -i HEAD~2`**:
   Объединение двух локальных коммитов в один с помощью команды `squash`.
6. **`git format-patch` и `git apply`**:
   - В ветке `dev3` создана серия из 2-х коммитов: добавление `constants.py` (`b31b909`) и `stats.py` (`5513d51`).
   - Сгенерированы патчи:
     ```bash
     git format-patch -2 dev3 -o patches/
     ```
     Созданы файлы:
     - `0001-feat-constants-add-mathematical-constants.patch`
     - `0002-feat-stats-add-average-calculation-utility.patch`
   - Патчи применены в ветку `main`:
     ```bash
     git apply patches/0001-*.patch patches/0002-*.patch
     git add constants.py stats.py
     git commit -m "feat(core): apply patches from dev3 (constants & stats) and add tests"
     git push origin main
     ```
     *Хэш коммита в `main`:* `bcd998b`

---

### Шаг 7. Вариант 4: Использование хуков для автоматизации процессов (Git Hooks)

Создан исполняемый скрипт `.git/hooks/pre-commit`, который запускается Git перед каждым выполнением `git commit`.

#### Листинг `.git/hooks/pre-commit`:
```bash
#!/bin/sh

echo "=========================================="
echo "[PRE-COMMIT HOOK] Starting automated checks..."
echo "=========================================="

# 1. Проверка форматирования Python-кода инструментом Black
echo "[HOOK: Step 1/2] Checking Python code formatting with black..."
python -m black --check .
BLACK_EXIT=$?

if [ $BLACK_EXIT -ne 0 ]; then
    echo "--------------------------------------------------------"
    echo " ОШИБКА: Код не отформатирован по стандарту Black!"
    echo "Запустите 'python -m black .' перед коммитом."
    echo "Коммит отклонен."
    echo "--------------------------------------------------------"
    exit 1
fi
echo " Форматирование кода соответствует стандарту Black."

# 2. Автоматический запуск тестов
echo "[HOOK: Step 2/2] Running automated tests..."
python -m unittest discover -p "test_*.py"
TESTS_EXIT=$?

if [ $TESTS_EXIT -ne 0 ]; then
    echo "--------------------------------------------------------"
    echo " ОШИБКА: Тесты завершились с ошибкой!"
    echo "Исправьте тесты перед фиксацией коммита."
    echo "Коммит отклонен."
    echo "--------------------------------------------------------"
    exit 1
fi
echo " Все автоматические тесты успешно пройдены."

echo "=========================================="
echo " Все проверки успешно пройдены! Коммит разрешен."
echo "=========================================="
exit 0
```

#### Настройка прав:
```bash
chmod +x .git/hooks/pre-commit
```

#### Результаты тестирования хука:

1. **Тест 1: Попытка коммита неотформатированного кода**
   - Добавлена функция с нарушением PEP 8 / Black:
     ```python
     def bad_style_function(  x,   y  ):
         return      x+y
     ```
   - Запуск `git commit -m "test bad format"`:
   - **Результат:**
     ```text
     would reformat utils.py
     1 file would be reformatted, 5 files would be left unchanged.
     --------------------------------------------------------
     ОШИБКА: Код не отформатирован по стандарту Black!
     Запустите 'python -m black .' перед коммитом.
     Коммит отклонен.
     --------------------------------------------------------
     ```
     Коммит успешно **заблокирован**.

2. **Тест 2: Попытка коммита кода с падающим тестом**
   - Код отформатирован, но в `test_app.py` добавлен ошибочный assert:
     ```python
     self.assertEqual(add(2, 3), 999)
     ```
   - Запуск `git commit -m "test failing test"`:
   - **Результат:**
     ```text
     [HOOK: Step 1/2] Checking Python code formatting with black...
     6 files would be left unchanged.
     Форматирование кода соответствует стандарту Black.
     [HOOK: Step 2/2] Running automated tests...
     FAIL: test_add (test_app.TestMathUtils.test_add)
     AssertionError: 5.0 != 999
     --------------------------------------------------------
     ОШИБКА: Тесты завершились с ошибкой!
     Коммит отклонен.
     --------------------------------------------------------
     ```
     Коммит успешно **заблокирован**.

3. **Тест 3: Корректный код и пройденные тесты**
   - Ошибочный тест исправлен, весь проект отформатирован `python -m black .`.
   - **Результат:**
     ```text
     [PRE-COMMIT HOOK] Starting automated checks...
     Форматирование кода соответствует стандарту Black.
     Все автоматические тесты успешно пройдены.
     Все проверки успешно пройдены! Коммит разрешен.
     [main 96ff6c7] style: format all files with black and configure pre-commit hook
     ```
     Коммит успешно **зафиксирован** и отправлен на GitHub.

---

## 3. Итоговый граф репозитория на GitHub

```text
* 96ff6c7 style: format all files with black and configure pre-commit hook
* bcd998b feat(core): apply patches from dev3 (constants & stats) and add tests
*   862d2af Merge branch 'dev1' into main: resolve conflict in utils.py
|\  
| * 28b31c2 feat(utils): update add with rounding by Person 1 in dev1
* |   2ff3705 Merge branch 'dev2' into main
|\ \  
| * | e29fb56 feat(app): add logging integration by Person 2 in dev2
| * | 7267082 feat(logger): add action logging with log levels (amended)
| |/  
| | * 5513d51 feat(stats): add average calculation utility
| | * b31b909 feat(constants): add mathematical constants
| |/  
|/|   
* | 86e7a18 feat(utils): update utils header and add func by Person 3 in dev3
|/  
| * a9a70bb feat(config): add configuration module in dev branch
|/  
* 4e8d425 feat(app): use subtract in main application and test suite
* a97736b feat(utils): add subtract function
* 421203b feat(app): add initial MathApp with 3 files (app.py, utils.py, test_app.py)
* bc97eb7 Add gitignore for simulation directories and artifacts
* 038dd27 Initial commit
```

Все ветки (`main`, `dev`, `dev1`, `dev2`, `dev3`) и коммиты успешно синхронизированы с удаленным репозиторием https://github.com/SL1dee36/NewRemoteRepository.
