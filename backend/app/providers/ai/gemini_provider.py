from collections.abc import AsyncGenerator
from typing import Any

import httpx

from app.core.config import settings
from app.providers.ai.base import AIProvider, ChatMessage, ModelCapabilities, StreamChunk


class GeminiProvider(AIProvider):
    name = "gemini"

    def __init__(self) -> None:
        self.capabilities = ModelCapabilities(
            streaming=True,
            tools=True,
            vision=True,
            json_mode=True,
            max_context_length=128000,
        )
        self.api_key = settings.google_api_key
        self.api_base = "https://generativelanguage.googleapis.com/v1beta"

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
        url = f"{self.api_base}/models/{model or 'gemini-2.0-flash'}:generateContent"
        payload = self._build_payload(
            messages, system_prompt, temperature, top_p, max_tokens, tools
        )

        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                params={"key": self.api_key},
                json=payload,
            )
            response.raise_for_status()
            data = response.json()

        text = ""
        candidates = data.get("candidates", [])
        if candidates:
            content = candidates[0].get("content", {})
            parts = content.get("parts", [])
            for part in parts:
                text += part.get("text", "")

        return ChatMessage(role="assistant", content=text)

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
        url = f"{self.api_base}/models/{model or 'gemini-2.0-flash'}:streamGenerateContent"
        payload = self._build_payload(
            messages, system_prompt, temperature, top_p, max_tokens, tools
        )

        async with httpx.AsyncClient() as client, client.stream(
            "POST",
            url,
            params={"key": self.api_key, "alt": "sse"},
            json=payload,
        ) as response:
            response.raise_for_status()
            async for line in response.aiter_lines():
                if line.startswith("data: "):
                    import json
                    data = json.loads(line[6:])
                    candidates = data.get("candidates", [])
                    if candidates:
                        content = candidates[0].get("content", {})
                        parts = content.get("parts", [])
                        for part in parts:
                            yield StreamChunk(content=part.get("text", ""))

    async def get_models(self) -> list[dict]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.api_base}/models",
                params={"key": self.api_key},
            )
            response.raise_for_status()
            data = response.json()
        return [
            {"id": m["name"], "name": m["displayName"]}
            for m in data.get("models", [])
        ]

    def _build_payload(
        self,
        messages: list[ChatMessage],
        system_prompt: str | None,
        temperature: float | None,
        top_p: float | None,
        max_tokens: int | None,
        _tools: list[dict] | None,
    ) -> dict:
        contents = []
        for msg in messages:
            contents.append({
                "role": "user" if msg.role == "user" else "model",
                "parts": [{"text": msg.content}],
            })

        payload: dict[str, Any] = {"contents": contents}
        if system_prompt:
            payload["systemInstruction"] = {
                "parts": [{"text": system_prompt}]
            }
        generation_config: dict = {}
        if temperature is not None:
            generation_config["temperature"] = temperature
        if top_p is not None:
            generation_config["topP"] = top_p
        if max_tokens is not None:
            generation_config["maxOutputTokens"] = max_tokens
        if generation_config:
            payload["generationConfig"] = generation_config
        return payload
