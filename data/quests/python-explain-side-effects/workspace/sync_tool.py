import os

def sync_data(source, target):
    try:
        if not os.path.exists(source):
            raise FileNotFoundError(f"Source {source} missing")
        # sync logic...
    except Exception as e:
        with open("sync_error.log", "a") as f:
            f.write(str(e) + "\n")
        return False
    return True
