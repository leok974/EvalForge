from pathlib import Path

def read_config(path_str: str) -> dict:
    """
    Read a line-based config file.
    Return dict {key: value} where lines are 'key=value'.
    If file missing, return empty dict and print 'CONFIG_MISSING'.
    """
    p = Path(path_str)
    if not p.exists():
        print("CONFIG_MISSING")
        return {}
    
    config = {}
    try:
        content = p.read_text(encoding="utf-8")
        for line in content.splitlines():
            line = line.strip()
            if not line or "=" not in line:
                continue
            k, v = line.split("=", 1)
            config[k.strip()] = v.strip()
    except Exception:
        pass # specific error handling not strictly required by spec, but safe I/O implies robust
        
    return config
