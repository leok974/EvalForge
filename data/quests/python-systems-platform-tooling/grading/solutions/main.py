def parse_semver(v):
    parts = v.split('.')
    if len(parts) != 3: raise ValueError("Invalid format")
    try:
        return tuple(map(int, parts))
    except:
        raise ValueError("Not integers")