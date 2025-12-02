from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    environment: str = "dev"  # "dev" | "staging" | "prod"
    dev_unlock_all_features: bool = False

    class Config:
        env_prefix = "EVALFORGE_"

settings = Settings()

def dev_unlock_all_enabled() -> bool:
    """
    Returns True if God Mode is enabled.
    Safety rail: Only allows True if environment is NOT 'prod'.
    """
    return settings.environment != "prod" and settings.dev_unlock_all_features
