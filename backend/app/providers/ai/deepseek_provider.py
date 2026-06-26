from openai import AsyncOpenAI

from app.core.config import settings
from app.providers.ai.base import ModelCapabilities
from app.providers.ai.openai_provider import OpenAIProvider


class DeepSeekProvider(OpenAIProvider):
    name = "deepseek"

    def __init__(self) -> None:
        self.capabilities = ModelCapabilities(
            streaming=True,
            tools=True,
            json_mode=True,
            max_context_length=128000,
        )
        self.client = AsyncOpenAI(
            api_key=settings.deepseek_api_key or "",
            base_url="https://api.deepseek.com",
        )

    async def get_models(self) -> list[dict]:
        return [
            {"id": "deepseek-chat", "name": "DeepSeek Chat"},
            {"id": "deepseek-reasoner", "name": "DeepSeek Reasoner"},
        ]
