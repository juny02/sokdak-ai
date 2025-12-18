from typing import Protocol


class LLMClient(Protocol):
    async def generate(self, messages: list[dict]) -> str:
        """
        messages:
            OpenAI/LLM 메시지 포맷
            [
                {
                    "role": "system",
                    "content": system_prompt  # persona + policy + summary
                },
                *history_messages, # 최근 대화 N개 (user/assistant)
                {
                    "role": "user",
                    "content": user_input
                }
            ]

        return:
            모델이 생성한 응답 텍스트
        """
        ...
