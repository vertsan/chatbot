from collections.abc import AsyncGenerator, Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.chat import Message
from app.providers.ai import ChatMessage, ProviderRegistry, StreamChunk
from app.providers.ai.registry import ProviderRegistry
from app.repositories.provider import AIModelRepository


class AIService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.model_repo = AIModelRepository(session)

    async def chat(
        self,
        messages: Sequence[Message],
        model_id: str | None = None,
        system_prompt: str | None = None,
        temperature: float | None = None,
        top_p: float | None = None,
        max_tokens: int | None = None,
    ) -> ChatMessage:
        provider, model = await self._resolve_provider(model_id)
        chat_messages = self._convert_messages(messages)

        return await provider.chat(
            messages=chat_messages,
            model=model,
            system_prompt=system_prompt,
            temperature=temperature,
            top_p=top_p,
            max_tokens=max_tokens,
        )

    async def stream_chat(
        self,
        messages: Sequence[Message],
        model_id: str | None = None,
        system_prompt: str | None = None,
        temperature: float | None = None,
        top_p: float | None = None,
        max_tokens: int | None = None,
    ) -> AsyncGenerator[StreamChunk, None]:
        provider, model = await self._resolve_provider(model_id)
        chat_messages = self._convert_messages(messages)

        async for chunk in provider.stream_chat(
            messages=chat_messages,
            model=model,
            system_prompt=system_prompt,
            temperature=temperature,
            top_p=top_p,
            max_tokens=max_tokens,
        ):
            yield chunk

    async def _resolve_provider(
        self, model_id: str | None
    ) -> tuple:
        if model_id:
            ai_model = await self.model_repo.get(model_id)
            if ai_model:
                provider = ProviderRegistry.get(
                    ai_model.provider.name
                )
                return provider, ai_model.model_id

        # Fall back to default
        for provider in ProviderRegistry.get_all().values():
            return provider, None

        raise ValueError("No AI providers available")

    def _convert_messages(
        self, messages: Sequence[Message]
    ) -> list[ChatMessage]:
        return [
            ChatMessage(role=msg.role, content=msg.content)
            for msg in messages
        ]
