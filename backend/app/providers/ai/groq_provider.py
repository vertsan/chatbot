from openai import AsyncOpenAI

from app.core.config import settings
from app.providers.ai.base import ModelCapabilities
from app.providers.ai.openai_provider import OpenAIProvider


class GroqProvider(OpenAIProvider):
    name = "groq"

    def __init__(self) -> None:
        self.capabilities = ModelCapabilities(
            streaming=True,
            tools=True,
            json_mode=True,
            max_context_length=128000,
        )
        self.client = AsyncOpenAI(
            api_key=settings.groq_api_key or "",
            base_url="https://api.groq.com/openai/v1",
        )

    async def get_models(self) -> list[dict]:
        return [
            {"id": "llama3-70b-8192", "name": "Llama 3 70B"},
            {"id": "llama3-8b-8192", "name": "Llama 3 8B"},
            {"id": "mixtral-8x7b-32768", "name": "Mixtral 8x7B"},
            {"id": "gemma2-9b-it", "name": "Gemma 2 9B"},
        ]
