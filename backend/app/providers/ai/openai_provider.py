from typing import Any, AsyncGenerator

from openai import AsyncOpenAI

from app.core.config import settings
from app.providers.ai.base import AIProvider, ChatMessage, ModelCapabilities, StreamChunk


class OpenAIProvider(AIProvider):
    name = "openai"

    def __init__(self) -> None:
        self.capabilities = ModelCapabilities(
            streaming=True,
            tools=True,
            vision=True,
            embeddings=True,
            json_mode=True,
            max_context_length=128000,
        )
        self.client = AsyncOpenAI(
            api_key=settings.openai_api_key,
            base_url=settings.openai_api_base,
        )

    async def chat(
        self,
        messages: list[ChatMessage],
        model: str | None = None,
        system_prompt: str | None = None,
        temperature: float | None = None,
        top_p: float | None = None,
        max_tokens: int | None = None,
        tools: list[dict] | None = None,
    ) -> ChatMessage:
        openai_messages = self._convert_messages(messages, system_prompt)
        kwargs = self._build_kwargs(model, temperature, top_p, max_tokens, tools)

        response = await self.client.chat.completions.create(
            messages=openai_messages,
            **kwargs,
        )
        choice = response.choices[0]
        return ChatMessage(
            role=choice.message.role or "assistant",
            content=choice.message.content or "",
            tool_calls=(
                [tc.model_dump() for tc in choice.message.tool_calls]
                if choice.message.tool_calls
                else None
            ),
        )

    async def stream_chat(
        self,
        messages: list[ChatMessage],
        model: str | None = None,
        system_prompt: str | None = None,
        temperature: float | None = None,
        top_p: float | None = None,
        max_tokens: int | None = None,
        tools: list[dict] | None = None,
    ) -> AsyncGenerator[StreamChunk, None]:
        openai_messages = self._convert_messages(messages, system_prompt)
        kwargs = self._build_kwargs(model, temperature, top_p, max_tokens, tools)

        stream = await self.client.chat.completions.create(
            messages=openai_messages,
            stream=True,
            stream_options={"include_usage": True},
            **kwargs,
        )
        async for chunk in stream:
            delta = chunk.choices[0].delta if chunk.choices else None
            content = delta.content or "" if delta else ""
            finish = (
                chunk.choices[0].finish_reason
                if chunk.choices and chunk.choices[0].finish_reason
                else None
            )
            yield StreamChunk(
                content=content,
                done=finish is not None,
                finish_reason=finish,
                input_tokens=chunk.usage.prompt_tokens if chunk.usage else None,
                output_tokens=chunk.usage.completion_tokens if chunk.usage else None,
            )

    async def get_models(self) -> list[dict]:
        response = await self.client.models.list()
        return [
            {"id": m.id, "name": m.id, "owned_by": m.owned_by}
            for m in response.data
        ]

    def _convert_messages(
        self, messages: list[ChatMessage], system_prompt: str | None
    ) -> list[dict]:
        result: list[dict] = []
        if system_prompt:
            result.append({"role": "system", "content": system_prompt})
        for msg in messages:
            entry: dict = {"role": msg.role, "content": msg.content}
            if msg.tool_calls:
                entry["tool_calls"] = msg.tool_calls
            if msg.tool_call_id:
                entry["tool_call_id"] = msg.tool_call_id
            result.append(entry)
        return result

    def _build_kwargs(
        self,
        model: str | None,
        temperature: float | None,
        top_p: float | None,
        max_tokens: int | None,
        tools: list[dict] | None,
    ) -> dict:
        kwargs: dict[str, Any] = {}
        kwargs["model"] = model or "gpt-4o"
        if temperature is not None:
            kwargs["temperature"] = temperature
        if top_p is not None:
            kwargs["top_p"] = top_p
        if max_tokens is not None:
            kwargs["max_tokens"] = max_tokens
        if tools:
            kwargs["tools"] = tools
        return kwargs
