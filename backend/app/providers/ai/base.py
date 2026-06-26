from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator
from dataclasses import dataclass, field


@dataclass
class ChatMessage:
    role: str
    content: str
    tool_calls: list[dict] | None = None
    tool_call_id: str | None = None


@dataclass
class StreamChunk:
    content: str = ""
    done: bool = False
    finish_reason: str | None = None
    input_tokens: int | None = None
    output_tokens: int | None = None


@dataclass
class ModelCapabilities:
    streaming: bool = True
    tools: bool = False
    vision: bool = False
    embeddings: bool = False
    json_mode: bool = False
    max_context_length: int = 4096


class AIProvider(ABC):
    name: str = ""
    capabilities: ModelCapabilities = field(default_factory=ModelCapabilities)

    @abstractmethod
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
        ...

    @abstractmethod
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
        ...

    @abstractmethod
    async def get_models(self) -> list[dict]:
        ...

    async def count_tokens(self, text: str) -> int:
        return len(text) // 4
