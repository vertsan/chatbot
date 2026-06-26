from collections.abc import AsyncGenerator
from typing import Any

import httpx

from app.core.config import settings
from app.providers.ai.base import AIProvider, ChatMessage, ModelCapabilities, StreamChunk


class AnthropicProvider(AIProvider):
    name = "anthropic"

    def __init__(self) -> None:
        self.capabilities = ModelCapabilities(
            streaming=True,
            tools=True,
            vision=True,
            json_mode=True,
            max_context_length=200000,
        )
        self.api_key = settings.anthropic_api_key
        self.api_base = "https://api.anthropic.com/v1"

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
        headers = self._headers()
        payload = self._build_payload(
            messages, model, system_prompt, temperature, top_p, max_tokens, tools
        )

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.api_base}/messages", headers=headers, json=payload
            )
            response.raise_for_status()
            data = response.json()

        content = ""
        for block in data.get("content", []):
            if block.get("type") == "text":
                content += block.get("text", "")

        return ChatMessage(role="assistant", content=content)

    async def stream_chat(
        self,
        messages: list[ChatMessage],
        model: str | None = None,
        system_prompt: str | None = None,
        temperature: float | None = None,
        top_p: float | None = None,
        max_tokens: int | None = None,
        tools: list[dict] | None = None,
    ) -> AsyncGenerator[StreamChunk]:
        headers = self._headers()
        headers["Accept"] = "text/event-stream"
        payload = self._build_payload(
            messages, model, system_prompt, temperature, top_p, max_tokens, tools
        )
        payload["stream"] = True

        async with httpx.AsyncClient() as client, client.stream(
            "POST",
            f"{self.api_base}/messages",
            headers=headers,
            json=payload,
        ) as response:
            response.raise_for_status()
            async for line in response.aiter_lines():
                if line.startswith("data: "):
                    import json
                    data = json.loads(line[6:])
                    if data.get("type") == "content_block_delta":
                        delta = data.get("delta", {})
                        if delta.get("type") == "text_delta":
                            yield StreamChunk(content=delta.get("text", ""))

    async def get_models(self) -> list[dict]:
        return [
            {"id": "claude-3-opus-20240229", "name": "Claude 3 Opus"},
            {"id": "claude-3-sonnet-20240229", "name": "Claude 3 Sonnet"},
            {"id": "claude-3-haiku-20240307", "name": "Claude 3 Haiku"},
            {"id": "claude-3-5-sonnet-20241022", "name": "Claude 3.5 Sonnet"},
        ]

    def _headers(self) -> dict:
        return {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
        }

    def _build_payload(
        self,
        messages: list[ChatMessage],
        model: str | None,
        system_prompt: str | None,
        temperature: float | None,
        top_p: float | None,
        max_tokens: int | None,
        tools: list[dict] | None,
    ) -> dict:
        payload: dict[str, Any] = {}
        payload["model"] = model or "claude-3-5-sonnet-20241022"
        payload["max_tokens"] = max_tokens or 4096
        anthropic_messages = []
        for msg in messages:
            if msg.role == "system":
                payload["system"] = payload.get("system", "") + msg.content
            else:
                anthropic_messages.append(
                    {"role": msg.role, "content": msg.content}
                )
        payload["messages"] = anthropic_messages
        if system_prompt:
            payload["system"] = system_prompt
        if temperature is not None:
            payload["temperature"] = temperature
        if top_p is not None:
            payload["top_p"] = top_p
        if tools:
            payload["tools"] = tools
        return payload
