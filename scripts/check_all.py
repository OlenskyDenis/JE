#!/usr/bin/env python
"""
Healthcheck and Quality Gate verification script for JE project.
Runs:
  1. Python syntax & bytecode compilation check (compileall)
  2. JavaScript syntax & integrity check (Node.js --check)
  3. Ruff static analysis & linting (if available)
  4. Mypy static type checking (optional / if available)
  5. Pytest unit & integration test suites (optionally E2E Playwright)

Usage:
    python scripts/check_all.py          # Fast verification (Syntax + JS + Lint + Pytest)
    python scripts/check_all.py --e2e    # Full verification including Playwright E2E
    python scripts/check_all.py --mypy   # Include strict mypy type checking
    python scripts/check_all.py --fix    # Auto-fix linting issues where possible
"""

import sys
import os
import time
import shutil
import argparse
import subprocess
import compileall
from pathlib import Path

# Project root directory
REPO_ROOT = Path(__file__).resolve().parent.parent


def print_step(title: str):
    print(f"\n\033[1;36m===> {title}\033[0m")


def print_success(msg: str):
    print(f"\033[1;32m[PASS] {msg}\033[0m")


def print_warn(msg: str):
    print(f"\033[1;33m[WARN] {msg}\033[0m")


def print_error(msg: str):
    print(f"\033[1;31m[FAIL] {msg}\033[0m", file=sys.stderr)


def check_python_syntax() -> bool:
    print_step("Step 1: Python Syntax & Bytecode Compilation Check")
    src_dir = str(REPO_ROOT / "src")
    tests_dir = str(REPO_ROOT / "tests")

    success_src = compileall.compile_dir(src_dir, quiet=1, force=False)
    success_tests = compileall.compile_dir(tests_dir, quiet=1, force=False)

    if success_src and success_tests:
        print_success("All Python source and test files compiled without syntax errors.")
        return True
    else:
        print_error("Syntax or bytecode compilation errors detected in Python files.")
        return False


def check_javascript_syntax() -> bool:
    print_step("Step 2: JavaScript Syntax & Integrity Check (Node.js)")
    js_dir = REPO_ROOT / "src" / "web" / "js"
    if not js_dir.exists():
        print_warn(f"JavaScript directory not found at {js_dir}")
        return True

    node_bin = shutil.which("node")
    if not node_bin:
        print_warn("Node.js is not found in PATH. Skipping Node syntax verification.")
        return True

    js_files = sorted(list(js_dir.glob("*.js")))
    if not js_files:
        print_warn("No JavaScript files found to check.")
        return True

    all_passed = True
    for js_file in js_files:
        res = subprocess.run([node_bin, "--check", str(js_file)], capture_output=True, text=True)
        if res.returncode != 0:
            print_error(f"JS Syntax Error in {js_file.name}:\n{res.stderr}")
            all_passed = False

    if all_passed:
        print_success(f"All {len(js_files)} JavaScript module files passed syntax check.")
        return True
    return False


def check_ruff_lint(fix: bool = False, check_format: bool = False) -> bool:
    print_step("Step 3: Ruff Static Analysis & Lint Check")
    
    # Check if ruff binary or module is available
    ruff_bin = shutil.which("ruff")
    if ruff_bin:
        base_cmd = [ruff_bin]
    else:
        # Check if python -m ruff works
        check_mod = subprocess.run([sys.executable, "-c", "import ruff"], capture_output=True)
        if check_mod.returncode != 0:
            print_warn("Ruff is not installed in Python environment. (Install via 'pip install ruff')")
            return True
        base_cmd = [sys.executable, "-m", "ruff"]

    if fix:
        subprocess.run(base_cmd + ["format", "src", "tests"], cwd=str(REPO_ROOT), capture_output=True)
        subprocess.run(base_cmd + ["check", "--fix", "src", "tests"], cwd=str(REPO_ROOT), capture_output=True)

    cmd_lint = base_cmd + ["check", "src", "tests"]
    res = subprocess.run(cmd_lint, cwd=str(REPO_ROOT), capture_output=True, text=True)
    if res.returncode != 0:
        print_error(f"Ruff detected linting issues:\n{res.stdout}\n{res.stderr}")
        return False

    if check_format:
        cmd_fmt = base_cmd + ["format", "--check", "src", "tests"]
        res_fmt = subprocess.run(cmd_fmt, cwd=str(REPO_ROOT), capture_output=True, text=True)
        if res_fmt.returncode != 0:
            print_error(f"Ruff detected code formatting issues:\n{res_fmt.stdout}\n{res_fmt.stderr}")
            return False

    print_success("Ruff static analysis: Zero issues found.")
    return True



def check_mypy_types() -> bool:
    print_step("Step 4: Mypy Static Type Validation")
    mypy_bin = shutil.which("mypy")
    if mypy_bin:
        cmd = [mypy_bin, "src/hierarchy_lib", "--ignore-missing-imports"]
    else:
        check_mod = subprocess.run([sys.executable, "-c", "import mypy"], capture_output=True)
        if check_mod.returncode != 0:
            print_warn("Mypy is not installed in Python environment. (Install via 'pip install mypy')")
            return True
        cmd = [sys.executable, "-m", "mypy", "src/hierarchy_lib", "--ignore-missing-imports"]

    res = subprocess.run(cmd, cwd=str(REPO_ROOT), capture_output=True, text=True)
    if res.returncode == 0:
        print_success("Mypy type checking: All checked modules passed.")
        return True
    else:
        print_warn(f"Mypy reported type issues:\n{res.stdout}")
        return True  # Informative


def run_pytest(include_e2e: bool = False) -> bool:
    print_step("Step 5: Pytest Test Suite Execution")
    test_paths = ["tests/unit", "tests/integration"]
    if include_e2e:
        test_paths.append("tests/e2e")
        print("Running: Unit, Integration, and E2E Playwright tests...")
    else:
        print("Running: Unit and Integration tests (use --full or --e2e for browser suite)...")

    cmd = [sys.executable, "-m", "pytest"] + test_paths
    result = subprocess.run(cmd, cwd=str(REPO_ROOT))

    if result.returncode == 0:
        print_success("All executed test suites passed successfully.")
        return True
    else:
        print_error(f"Pytest failed with exit code {result.returncode}.")
        return False


def main():
    parser = argparse.ArgumentParser(description="JE Quality Gate & Healthcheck Runner")
    parser.add_argument("-q", "--quick", action="store_true", help="Run fast verification (unit & integration tests only)")
    parser.add_argument("-f", "--full", action="store_true", help="Run full verification (including Playwright E2E)")
    parser.add_argument("--e2e", action="store_true", help="Include Playwright E2E browser tests")
    parser.add_argument("--mypy", action="store_true", help="Run Mypy static type checker")
    parser.add_argument("--fix", action="store_true", help="Auto-fix linting & formatting issues with Ruff")
    parser.add_argument("--format", action="store_true", help="Strictly verify code formatting with Ruff")
    parser.add_argument("--no-lint", action="store_true", help="Skip Ruff linting step")
    args = parser.parse_args()

    include_e2e = args.full or args.e2e

    start_time = time.time()
    mode_label = "FULL" if include_e2e else "QUICK"
    print(f"\033[1;35m--- JE Project Health Check & Quality Gate [{mode_label} MODE] ---\033[0m")

    # 1. Python Syntax
    if not check_python_syntax():
        sys.exit(1)

    # 2. JavaScript Syntax
    if not check_javascript_syntax():
        sys.exit(1)

    # 3. Ruff Linting & Formatting
    if not args.no_lint:
        if not check_ruff_lint(fix=args.fix, check_format=args.format):
            sys.exit(1)


    # 4. Mypy Type Checking (if requested)
    if args.mypy:
        check_mypy_types()

    # 5. Pytest Execution
    if not run_pytest(include_e2e=include_e2e):
        sys.exit(1)

    elapsed = time.time() - start_time
    print(f"\n\033[1;32m====================================================\033[0m")
    print(f"\033[1;32m   ALL QUALITY GATES PASSED (Time: {elapsed:.2f}s)   \033[0m")
    print(f"\033[1;32m====================================================\033[0m\n")


if __name__ == "__main__":
    main()

