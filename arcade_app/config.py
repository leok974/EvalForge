"""
Centralized configuration for EvalForge.
Handles environment-aware defaults for local dev vs Docker vs production.
"""
import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    environment: str = "dev"  # "dev" | "staging" | "prod"
    dev_unlock_all_features: bool = False
    public_base_url: str | None = None
    intent_oracle_eval_token: str | None = None
    antigravity_base_url: str | None = None
    antigravity_api_token: str | None = None

    model_config = SettingsConfigDict(env_prefix="EVALFORGE_")


settings = Settings()


def dev_unlock_all_enabled() -> bool:
    """
    Returns True if God Mode is enabled.
    Safety rail: Only allows True if environment is NOT 'prod'.
    """
    return settings.environment != "prod" and settings.dev_unlock_all_features


def get_database_url() -> str:
    """
    Returns the database URL with smart defaults.
    
    Priority:
    1. DATABASE_URL env var (explicit override)
    2. If IN_DOCKER=1 -> use docker service name 'db'
    3. Else -> localhost (for local dev outside Docker)
    """
    if url := os.getenv("DATABASE_URL"):
        return url
    
    in_docker = os.getenv("IN_DOCKER") == "1"
    host = "db" if in_docker else "127.0.0.1"
    port = 5432 if in_docker else 5435  # Local dev uses 5435
    
    # Default credentials (override via DATABASE_URL if needed)
    user = "evalforge_app"
    password = "evalforge_dev"
    dbname = "evalforge"
    
    return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{dbname}"


def get_redis_url() -> str:
    """
    Returns the Redis URL with smart defaults.
    
    Priority:
    1. REDIS_URL env var (explicit override)
    2. If IN_DOCKER=1 -> use docker service name 'redis'
    3. Else -> 127.0.0.1 (for local dev outside Docker)
    """
    if url := os.getenv("REDIS_URL"):
        return url
    
    in_docker = os.getenv("IN_DOCKER") == "1"
    host = "redis" if in_docker else "127.0.0.1"
    port = 6379
    db = 0
    
    return f"redis://{host}:{port}/{db}"


def is_development() -> bool:
    """Returns True if running in development mode."""
    return os.getenv("ENV", "development") == "development"


def should_auto_init_db() -> bool:
    """Returns True if the database should be auto-initialized on startup."""
    # Only auto-init in dev mode OR if explicitly requested
    return os.getenv("AUTO_INIT_DB") == "1" or (is_development() and os.getenv("SKIP_AUTO_INIT") != "1")


# Export convenient constants
DATABASE_URL = get_database_url()
REDIS_URL = get_redis_url()
IS_DEV = is_development()
AUTO_INIT_DB = should_auto_init_db()

# Print config on import for debugging (only in dev)
if IS_DEV:
    print(f"[EvalForge Config] DATABASE_URL: {DATABASE_URL}")
    print(f"[EvalForge Config] REDIS_URL: {REDIS_URL}")
    print(f"[EvalForge Config] AUTO_INIT_DB: {AUTO_INIT_DB}")

