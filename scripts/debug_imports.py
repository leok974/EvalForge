
import sys
import os

sys.path.append(os.getcwd())

try:
    from arcade_app.routers import routes_codex
    print(f"routes_codex file: {routes_codex.__file__}")
    print(f"routes_codex router prefix: {routes_codex.router.prefix}")
    # Check if list_codex_entries exists in it
    if hasattr(routes_codex, 'list_codex_entries'):
        print("routes_codex HAS list_codex_entries (BAD - matches codex.py)")
    else:
        print("routes_codex converts get_codex_entry (GOOD)")
except Exception as e:
    print(f"Error importing routes_codex: {e}")

try:
    from arcade_app.routers import codex
    print(f"codex file: {codex.__file__}")
    print(f"codex router prefix: {codex.router.prefix}")
except Exception as e:
    print(f"Error importing codex: {e}")
