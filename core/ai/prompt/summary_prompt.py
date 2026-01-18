from typing import List, Optional

from app.chat.domain.entity import Message
from app.chat.domain.enum import Language
from core.ai.message import OpenAIMessage, OpenAIMessageFactory


class OpenAISummaryPrompt:
    """대화 요약용 프롬프트 빌더"""

    BASE_SYSTEM = (
        "You update an existing conversation summary. "
        "Preserve important facts, user intent, decisions, preferences, context. "
        "Be concise and factual. "
        "Do not add interpretation, advice, or assumptions. "
        "Do not include greetings or filler."
    )

    LANGUAGE_INSTRUCTIONS = {
        Language.KOREAN: "Write the summary in Korean.",
        Language.ENGLISH: "Write the summary in English.",
    }

    @classmethod
    def _build_system_prompt(
        cls,
        language: Language,
        previous_summary: Optional[str],
    ) -> str:
        """시스템 프롬프트를 조립합니다."""
        sections = [
            cls.BASE_SYSTEM,
            cls.LANGUAGE_INSTRUCTIONS[language],
        ]

        if previous_summary:
            sections.append(f"[Previous Summary]\n{previous_summary}")

        return "\n\n".join(sections)

    @classmethod
    def build(
        cls,
        *,
        previous_summary: Optional[str],
        history: List[Message],
        language: Language = Language.ENGLISH,
    ) -> List[OpenAIMessage]:
        """요약 메시지 리스트를 생성합니다."""
        messages: List[OpenAIMessage] = []

        # system prompt
        system_prompt = cls._build_system_prompt(language, previous_summary)
        messages.append(OpenAIMessageFactory.system(system_prompt))

        # new messages since last summary
        for msg in history:
            messages.append(OpenAIMessageFactory.from_domain(msg))

        # explicit update instruction
        messages.append(
            OpenAIMessageFactory.user(
                "Update the summary to include the new messages above."
            )
        )

        return messages
