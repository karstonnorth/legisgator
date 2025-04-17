import os, hashlib
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    MODEL: str = "gpt-4o-mini"
    MAX_PAYLOAD_KB: int = 64
    CACHE_PATH: str = ".cache"
    CACHE_TTL_HOURS: int = 24               # NEW ★
    GPT_TIMEOUT: int = 30
    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(case_sensitive=True, env_file=".env")

    @property
    def api_key_fingerprint(self) -> str:   # hashed for safe logs
        return hashlib.sha256(self.OPENAI_API_KEY.encode()).hexdigest()[:12]

@lru_cache
def get_settings() -> Settings:
    cfg = Settings()
    return cfg
