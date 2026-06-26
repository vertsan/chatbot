import os

os.environ.setdefault("SECRET_KEY", "test-secret-key")
os.environ.setdefault(
    "DATABASE_URL",
    "postgresql+asyncpg://chatbot:chatbot@localhost:5432/chatbot_test",
)
os.environ.setdefault("JWT_SECRET_KEY", "test-jwt-secret")
os.environ.setdefault("ENVIRONMENT", "development")
os.environ.setdefault("REDIS_URL", "redis://localhost:6379/0")
