# Tasks: Spec 032 Test Fixtures Suite, Knowledge Base & Pre-Commit Quality Automation

## Phase 1: Test Fixtures Suite
- [x] 1.1 Створити генератор тестових Excel-файлів `tests/fixtures/generate_fixtures.py`.
- [x] 1.2 Згенерувати 5 еталонних `.xlsx` файлів у `tests/fixtures/excel_samples/`.
- [x] 1.3 Створити `tests/unit/test_excel_fixtures.py` з повним покриттям усіх 5 файлів.

## Phase 2: Quality Automation & Git Hooks
- [x] 2.1 Оновити `scripts/check_all.py` з підтримкою прапорців `--quick` / `--full` та `check_all.ps1`.
- [x] 2.2 Створити `scripts/install_git_hooks.py` для швидкого встановлення pre-commit хука.
- [x] 2.3 Перевірити роботу pre-commit хука та статус `check_all.py`.

## Phase 3: Project Knowledge Base
- [x] 3.1 Створити `docs/KNOWLEDGE.md` з детальним описом архітектури, Eel IPC, OpenPyXL та життєвого циклу.

## Phase 4: Verification & Final Registry Update
- [x] 4.1 Оновити реєстр специфікацій у `specs/README.md`.
- [x] 4.2 Запустити `python scripts/check_all.py --full` та переконатися у проходженні 100% тестів та лінтерів.
- [x] 4.3 Створити підсумковий walkthrough-артефакт.
