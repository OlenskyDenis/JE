#!/usr/bin/env python
"""
Git Pre-Commit Hook Installer for JE project.
Installs a pre-commit hook that automatically runs `python scripts/check_all.py --quick`
before any commit is finalized, ensuring continuous adherence to QualityGate.md.
"""

import os
import stat
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
GIT_DIR = REPO_ROOT / ".git"
HOOKS_DIR = GIT_DIR / "hooks"
PRE_COMMIT_FILE = HOOKS_DIR / "pre-commit"

HOOK_CONTENT = """#!/usr/bin/env bash
# ==============================================================================
# JE Pre-Commit Quality Gate Hook
# ==============================================================================
echo "===> [Hook] Running Pre-Commit Quality Gate (Syntax + JS + Ruff + Pytest)..."

python scripts/check_all.py --quick
EXIT_CODE=$?

if [ $EXIT_CODE -ne 0 ]; then
    echo ""
    echo "================================================================================"
    echo " [ERROR] Pre-Commit Quality Gate FAILED (Exit code $EXIT_CODE)!"
    echo " Please resolve syntax errors, linting issues, or failing tests before committing."
    echo " To bypass this check in an emergency, use: git commit --no-verify"
    echo "================================================================================"
    exit 1
fi

echo "===> [Hook] Pre-commit verification passed. Proceeding with commit."
exit 0
"""


def install_hooks() -> bool:
    """Installs the pre-commit hook into .git/hooks/pre-commit."""
    if not GIT_DIR.exists():
        print(f"[ERROR] .git directory not found at: {GIT_DIR}. Are you in a Git repository?", file=sys.stderr)
        return False

    HOOKS_DIR.mkdir(parents=True, exist_ok=True)

    # Write hook content using LF newlines for git bash compatibility
    with open(PRE_COMMIT_FILE, "w", encoding="utf-8", newline="\n") as f:
        f.write(HOOK_CONTENT)

    # Set executable permissions (0o755)
    current_stat = os.stat(PRE_COMMIT_FILE)
    os.chmod(PRE_COMMIT_FILE, current_stat.st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    print(f"\033[1;32m[SUCCESS] Pre-commit hook installed at:\033[0m {PRE_COMMIT_FILE}")
    print("  -> The hook will automatically run 'python scripts/check_all.py --quick' before every commit.")
    print("  -> To bypass verification if necessary: 'git commit --no-verify'\n")
    return True


if __name__ == "__main__":
    success = install_hooks()
    sys.exit(0 if success else 1)
