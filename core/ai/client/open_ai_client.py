from typing import Dict, List

from openai import AsyncOpenAI


class OpenAIClient:
    """
    OpenAI Chat Completion client.
    - OpenAI SDK 호출만 담당
    """

    def __init__(self) -> None:
        self._client = AsyncOpenAI(
            api_key="API_KEY",  # TODO: 환경변수 추가
        )

    async def generate(self, messages: List[Dict[str, str]]) -> str:
        """
        messages:
            [
                {"role": "system", "content": "..."},
                {"role": "user", "content": "..."},
                {"role": "assistant", "content": "..."},
            ]

        return:
            assistant 응답 텍스트
        """
        response = await self._client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=messages,
            temperature=0.7,
        )

        return response.choices[0].message.content
