from app.character.domain.valueobject import Persona
from app.chat.domain.entity.message import Message
from app.chat.domain.enum import Language
from core.ai.client import OpenAIClient
from core.ai.prompt import OpenAIChatPrompt, OpenAISummaryPrompt


class OpenAIService:
    def __init__(
        self,
        client: OpenAIClient,
    ) -> None:
        self._client = client

    async def chat(
        self,
        *,
        persona: Persona,
        summary: str | None,
        history: list[Message],
        user_input: str,
        language: Language,
    ) -> str:
        messages = OpenAIChatPrompt.build(
            persona=persona,
            summary=summary,
            history=history,
            user_input=user_input,
            language=language,
        )

        return await self._client.generate(messages)

    async def summarize(
        self,
        *,
        previous_summary: str | None,
        recent_messages: list[Message],
        language: Language,
    ) -> str:
        messages = OpenAISummaryPrompt.build(
            previous_summary=previous_summary,
            history=recent_messages,
            language=language,
        )

        return await self._client.generate(messages)
