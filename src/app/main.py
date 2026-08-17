"""Eel Desktop Application Entry Point."""

import os
import sys

# Ensure pure python fallback for gevent if DLL extensions are blocked
os.environ.setdefault("PURE_PYTHON", "1")

import eel

import src.app.eel_bridge  # noqa: F401 - Register all @eel.expose endpoints with Eel


def main():
    """Initializes and launches the Eel desktop UI."""
    web_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "web")
    if not os.path.exists(web_dir):
        print(f"Error: Web directory not found at {web_dir}", file=sys.stderr)
        sys.exit(1)

    eel.init(web_dir)

    print("Launching Database Hierarchy Creator Application...")
    try:
        # Launch Chrome/Chromium app or fallback to default browser
        eel.start("index.html", size=(1200, 800), port=0)
    except (SystemExit, KeyboardInterrupt):
        print("Application closed.")


if __name__ == "__main__":
    main()
