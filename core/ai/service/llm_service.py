from typing import Protocol

from app.character.domain.valueobject.persona import Persona
from app.chat.domain.entity.message import Message
from app.chat.domain.enum import Language


class LLMService(Protocol):
    async def chat(
        self,
        *,
        persona: Persona,
        summary: str | None,
        history: list[Message],
        user_input: str,
        language: Language,
    ) -> str: ...

    async def summarize(
        self,
        *,
        previous_summary: str | None,
        recent_messages: list[Message],
        language: Language,
    ) -> str: ...
