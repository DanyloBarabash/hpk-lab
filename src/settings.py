from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    redis_url: str | None = None
    redis_TTL: int = 60  # cache time
    environment: str = "development"

    model_config = ConfigDict(
        extra="allow",
        env_file=".env",
        env_file_encoding="utf-8",
    )

    # database settings (postgres)
    pg_host: str = "localhost"
    pg_port: int = 5432
    pg_username: str = "postgres"
    pg_password: str = "postgres"
    pg_db_name: str = "postgres"
    pg_db_driver: str = "postgresql"

    @property
    def postgres(self):
        return (
            f"{self.pg_db_driver}+asyncpg://{self.pg_username}:{self.pg_password}@"
            f"{self.pg_host}:{self.pg_port}/{self.pg_db_name}"
        )

    @property
    def postgres_sync(self):
        return (
            f"postgresql://{self.pg_username}:{self.pg_password}@"
            f"{self.pg_host}:{self.pg_port}/{self.pg_db_name}"
        )


settings = Settings()
