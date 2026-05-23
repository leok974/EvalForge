import os

def connect():
    port = os.getenv("DB_PORT", "5432")
    return f"Connected to port {port}"

if __name__ == "__main__":
    print(connect())
