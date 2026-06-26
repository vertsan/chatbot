from typing import Any, AsyncGenerator

import httpx

from app.core.config import settings
from app.providers.ai.base import AIProvider, ChatMessage, ModelCapabilities, StreamChunk


class OllamaProvider(AIProvider):
    name = "ollama"

    def __init__(self) -> None:
        self.capabilities = ModelCapabilities(
            streaming=True,
            tools=True,
            vision=True,
            json_mode=True,
            max_context_length=8192,
        )
        self.base_url = settings.ollama_base_url

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
        payload = self._build_payload(
            messages, model, system_prompt, temperature, top_p, max_tokens, tools
        )

        async with httpx.AsyncClient(base_url=self.base_url) as client:
            response = await client.post("/api/chat", json=payload)
            response.raise_for_status()
            data = response.json()

        return ChatMessage(
            role="assistant",
            content=data.get("message", {}).get("content", ""),
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
        payload = self._build_payload(
            messages, model, system_prompt, temperature, top_p, max_tokens, tools
        )
        payload["stream"] = True

        async with httpx.AsyncClient(base_url=self.base_url) as client:
            async with client.stream("POST", "/api/chat", json=payload) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if not line:
                        continue
                    import json
                    data = json.loads(line)
                    content = data.get("message", {}).get("content", "")
                    done = data.get("done", False)
                    yield StreamChunk(
                        content=content,
                        done=done,
                        finish_reason="stop" if done else None,
                    )

    async def get_models(self) -> list[dict]:
        async with httpx.AsyncClient(base_url=self.base_url) as client:
            response = await client.get("/api/tags")
            response.raise_for_status()
            data = response.json()
        return [
            {"id": m["name"], "name": m["name"]}
            for m in data.get("models", [])
        ]

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
        payload["model"] = model or "llama3.2"
        ollama_messages = []
        if system_prompt:
            ollama_messages.append({"role": "system", "content": system_prompt})
        for msg in messages:
            ollama_messages.append({"role": msg.role, "content": msg.content})
        payload["messages"] = ollama_messages
        options: dict = {}
        if temperature is not None:
            options["temperature"] = temperature
        if top_p is not None:
            options["top_p"] = top_p
        if max_tokens is not None:
            options["num_predict"] = max_tokens
        if options:
            payload["options"] = options
        if tools:
            payload["tools"] = tools
        return payload
