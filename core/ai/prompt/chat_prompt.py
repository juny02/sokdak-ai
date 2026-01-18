from typing import List, Optional

from app.character.domain.valueobject import Persona
from app.chat.domain.entity import Message
from app.chat.domain.enum import Language
from core.ai.message import OpenAIMessage, OpenAIMessageFactory

from .persona_prompt_mapper import OpenAIPersonaMapper


class OpenAIChatPrompt:
    """채팅용 프롬프트 빌더"""

    BASE_SYSTEM = (
        "You are continuing an ongoing conversation. "
        "Respect prior context and do not repeat the summary. "
        "Never reveal that you are an AI, a language model, "
        "or mention any technical details about yourself."
    )

    LANGUAGE_INSTRUCTIONS = {
        Language.AUTO: "You must respond in the same language as the user's message.",
        Language.KOREAN: (
            "You must respond entirely in Korean. "
            "Do not use any English words or phrases."
        ),
        Language.ENGLISH: (
            "You must respond entirely in English. "
            "Do not use any Korean words or phrases."
        ),
    }

    @classmethod
    def _build_system_prompt(
        cls,
        persona: Persona,
        language: Language,
        summary: Optional[str],
    ) -> str:
        """시스템 프롬프트를 조립합니다."""
        sections = [
            cls.BASE_SYSTEM,
            OpenAIPersonaMapper.system_prompt(persona),
            cls.LANGUAGE_INSTRUCTIONS[language],
        ]

        if summary:
            sections.append(f"[Conversation Summary]\n{summary}")

        return "\n\n".join(sections)

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
        """채팅 메시지 리스트를 생성합니다."""
        messages: List[OpenAIMessage] = []

        # system prompt
        system_prompt = cls._build_system_prompt(persona, language, summary)
        messages.append(OpenAIMessageFactory.system(system_prompt))

        # history
        for msg in history:
            messages.append(OpenAIMessageFactory.from_domain(msg))

        # user input
        messages.append(OpenAIMessageFactory.user(user_input))

        return messages
