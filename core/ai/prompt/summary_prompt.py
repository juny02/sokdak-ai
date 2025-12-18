from typing import List

from app.chat.domain.entity import Message
from app.chat.domain.enum import Language
from core.ai.message import OpenAIMessage, OpenAIMessageFactory


class OpenAISummaryPrompt:
    BASE_SYSTEM = (
        "You update an existing conversation summary.\n"
        "Preserve important facts, user intent, decisions, preferences, context.\n"
        "Be concise and factual.\n"
        "Do NOT add interpretation, advice, or assumptions.\n"
        "Do NOT include greetings or filler."
    )

    @classmethod
    # 영어를 기본값으로 설정
    def build(
        cls,
        *,
        previous_summary: str | None,
        history: List[Message],
        language: Language = Language.ENGLISH,
    ) -> List[OpenAIMessage]:
        messages: List[OpenAIMessage] = []

        # base system
        messages.append(OpenAIMessageFactory.system(cls.BASE_SYSTEM))

        # language
        messages.append(OpenAIMessageFactory.set_language(language))

        # previous summary (있을 때만)
        if previous_summary:
            messages.append(
                OpenAIMessageFactory.system(f"Previous summary:\n{previous_summary}")
            )

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
