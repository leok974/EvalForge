from pathlib import Path

def read_config(path_str: str) -> dict:
    """Read a key=value config file, returning {} if the file is missing."""
    try:
        lines = Path(path_str).read_text(encoding="utf-8").splitlines()
        return dict(line.split("=", 1) for line in lines if "=" in line)
    except FileNotFoundError:
        print("CONFIG_MISSING")
        return {}
