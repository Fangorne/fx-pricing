from functools import lru_cache

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # PostgreSQL — variables atomiques, URL construite automatiquement
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "fx_pricing"
    postgres_user: str = "fx_user"
    postgres_password: str = "changeme"

    # Accepte aussi DATABASE_URL directement (Docker injecte cette var)
    database_url: str = ""

    @computed_field  # type: ignore[prop-decorator]
    @property
    def effective_database_url(self) -> str:
        if self.database_url:
            return self.database_url
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    # Redis
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_url: str = ""

    @computed_field  # type: ignore[prop-decorator]
    @property
    def effective_redis_url(self) -> str:
        if self.redis_url:
            return self.redis_url
        return f"redis://{self.redis_host}:{self.redis_port}/0"

    # App
    secret_key: str = "changeme"
    debug: bool = False


@lru_cache
def get_settings() -> Settings:
    return Settings()
