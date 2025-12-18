from typing import List, Optional

from app.character.domain.valueobject import Persona
from app.chat.domain.entity import Message
from app.chat.domain.enum import Language
from core.ai.message import OpenAIMessage, OpenAIMessageFactory

from .persona_prompt_mapper import OpenAIPersonaMapper


class OpenAIChatPrompt:
    BASE_SYSTEM = (
        "You are continuing an ongoing conversation. "
        "Respect prior context and do not repeat the summary."
    )

    @classmethod
    def build(
        cls,
        *,
        persona: Persona,
        summary: Optional[str],
        history: List[Message],
        user_input: str,
        language: Language,
    ) -> List[OpenAIMessage]:
        messages: List[OpenAIMessage] = []

        # base system
        messages.append(OpenAIMessageFactory.system(cls.BASE_SYSTEM))

        # persona system (LLM-specific)
        messages.append(
            OpenAIMessageFactory.system(OpenAIPersonaMapper.system_prompt(persona))
        )

        # language system
        messages.append(
            OpenAIMessageFactory.system(f"Please respond only in {language.value}.")
        )

        # conversation summary
        if summary:
            messages.append(
                OpenAIMessageFactory.system(f"Conversation summary:\n{summary}")
            )

        # history
        for msg in history:
            messages.append(OpenAIMessageFactory.from_domain(msg))

        # current user input
        messages.append(OpenAIMessageFactory.user(user_input))

        return messages
