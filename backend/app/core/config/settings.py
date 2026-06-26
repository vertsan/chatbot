from enum import StrEnum
from pathlib import Path

from pydantic import PostgresDsn, RedisDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(StrEnum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


class StorageType(StrEnum):
    LOCAL = "local"
    S3 = "s3"


class VectorStoreType(StrEnum):
    PGVECTOR = "pgvector"
    CHROMA = "chroma"
    QDRANT = "qdrant"
    MILVUS = "milvus"


class LogFormat(StrEnum):
    JSON = "json"
    TEXT = "text"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    app_name: str = "Chatbot Platform"
    app_version: str = "1.0.0"
    debug: bool = False
    secret_key: str
    environment: Environment = Environment.DEVELOPMENT

    # Database
    database_url: PostgresDsn
    database_pool_size: int = 20
    database_max_overflow: int = 40

    # Redis
    redis_url: RedisDsn = "redis://localhost:6379/0"
    redis_max_connections: int = 50

    # Celery
    celery_broker_url: RedisDsn = "redis://localhost:6379/1"
    celery_result_backend: RedisDsn = "redis://localhost:6379/2"

    # Storage
    storage_type: StorageType = StorageType.S3
    s3_endpoint: str | None = None
    s3_access_key: str | None = None
    s3_secret_key: str | None = None
    s3_bucket: str = "chatbot-uploads"
    s3_region: str = "us-east-1"
    local_storage_path: Path = Path("uploads")

    # JWT
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30
    jwt_refresh_token_expire_days: int = 7

    # OAuth
    oauth_google_client_id: str | None = None
    oauth_google_client_secret: str | None = None
    oauth_github_client_id: str | None = None
    oauth_github_client_secret: str | None = None

    # AI Providers
    openai_api_key: str | None = None
    openai_api_base: str = "https://api.openai.com/v1"
    anthropic_api_key: str | None = None
    google_api_key: str | None = None
    azure_openai_api_key: str | None = None
    azure_openai_endpoint: str | None = None
    azure_openai_api_version: str = "2024-02-15-preview"
    huggingface_api_key: str | None = None
    groq_api_key: str | None = None
    deepseek_api_key: str | None = None
    ollama_base_url: str = "http://localhost:11434"
    vllm_base_url: str = "http://localhost:8000"
    lm_studio_base_url: str = "http://localhost:1234"

    # Embedding
    embedding_provider: str = "openai"
    openai_embedding_model: str = "text-embedding-3-small"
    ollama_embedding_model: str = "nomic-embed-text"

    # Vector Store
    vector_store_type: VectorStoreType = VectorStoreType.PGVECTOR
    chroma_host: str = "localhost"
    chroma_port: int = 8000
    qdrant_host: str = "localhost"
    qdrant_port: int = 6333
    milvus_host: str = "localhost"
    milvus_port: int = 19530

    # Rate Limiting
    rate_limit_enabled: bool = True
    rate_limit_requests: int = 100
    rate_limit_period: int = 60

    # CORS
    cors_origins: list[str] = ["http://localhost:5173", "http://localhost:3000"]

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, value: str | list[str]) -> list[str]:
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",")]
        return value

    # Logging
    log_level: str = "INFO"
    log_format: LogFormat = LogFormat.JSON

    # Observability
    sentry_dsn: str | None = None
    otel_enabled: bool = False
    otel_exporter_otlp_endpoint: str | None = None

    @property
    def is_production(self) -> bool:
        return self.environment == Environment.PRODUCTION

    @property
    def is_development(self) -> bool:
        return self.environment == Environment.DEVELOPMENT


settings = Settings()
