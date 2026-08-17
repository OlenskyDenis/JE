# Plan: Spec 032 Test Fixtures Suite, Knowledge Base & Pre-Commit Quality Automation

## 1. Архітектура та Розподіл по Шарах (Layering & Architecture)

### 1. Тестові Фікстури та Тестовий Набір
* **Шлях:** `tests/fixtures/generate_fixtures.py`, `tests/fixtures/excel_samples/*.xlsx`
* **Юніт тести:** `tests/unit/test_excel_fixtures.py`
* **Залежності:** `openpyxl`, `src.hierarchy_lib.adapters.excel_adapter.ExcelHierarchyAdapter`, `src.hierarchy_lib.services.path_parser.PathParser`.

### 2. Скрипти Перевірки та Автоматизації
* **Шлях:** `scripts/check_all.py`, `scripts/install_git_hooks.py`
* **Функціонал:**
  * Додати парсер аргументів (`argparse`) до `check_all.py` (`--quick`, `--full`, `--verbose`).
  * Створити скрипт `install_git_hooks.py`, що створює `.git/hooks/pre-commit` (bash/python скрипт).

### 3. Документація Бази Знань
* **Шлях:** `docs/KNOWLEDGE.md`
* **Зміст:** Квінтесенція архітектурних рішень, контрактів Eel, тонкощів OpenPyXL та рекомендацій щодо тестування.

---

## 2. Покроковий план виконання
1. Створити `tests/fixtures/generate_fixtures.py` та згенерувати 5 файлів у `tests/fixtures/excel_samples/`.
2. Створити `tests/unit/test_excel_fixtures.py` з ретельними перевірками імпорту, обробки типів та round-trip.
3. Оновити `scripts/check_all.py` для підтримки режимів `--quick` та `--full`.
4. Створити `scripts/install_git_hooks.py` та протестувати встановлення pre-commit хука.
5. Створити `docs/KNOWLEDGE.md`.
6. Оновити `specs/032-test-fixtures-and-quality-automation/tasks.md` та `specs/README.md`.
7. Запустити повну перевірку `python scripts/check_all.py --full`.
