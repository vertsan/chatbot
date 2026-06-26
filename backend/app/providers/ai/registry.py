from app.core.config import settings
from app.providers.ai import AIProvider
from app.providers.ai.anthropic_provider import AnthropicProvider
from app.providers.ai.deepseek_provider import DeepSeekProvider
from app.providers.ai.gemini_provider import GeminiProvider
from app.providers.ai.groq_provider import GroqProvider
from app.providers.ai.ollama_provider import OllamaProvider
from app.providers.ai.openai_provider import OpenAIProvider


class ProviderRegistry:
    _providers: dict[str, AIProvider] = {}

    @classmethod
    def register(cls, provider: AIProvider) -> None:
        cls._providers[provider.name] = provider

    @classmethod
    def get(cls, name: str) -> AIProvider:
        provider = cls._providers.get(name)
        if not provider:
            raise ValueError(f"Unknown provider: {name}")
        return provider

    @classmethod
    def get_all(cls) -> dict[str, AIProvider]:
        return cls._providers

    @classmethod
    def initialize(cls) -> None:
        if settings.openai_api_key:
            cls.register(OpenAIProvider())
        if settings.anthropic_api_key:
            cls.register(AnthropicProvider())
        if settings.google_api_key:
            cls.register(GeminiProvider())
        if settings.deepseek_api_key:
            cls.register(DeepSeekProvider())
        if settings.groq_api_key:
            cls.register(GroqProvider())
        # Always register Ollama
        cls.register(OllamaProvider())
