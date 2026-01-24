from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from core.setting import settings


class LangChainClient:
    """
    LangChain 기반 LLM client.
    - 기존 OpenAIClient와 동일한 인터페이스 유지
    """

    def __init__(
        self,
        model: str = "gpt-4.1-mini",
        temperature: float = 0.7,
    ) -> None:
        self._llm = ChatOpenAI(
            api_key=settings.OPEN_AI_API_KEY,
            model=model,
            temperature=temperature,
        )

    async def generate(self, messages: list[dict]) -> str:
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
        langchain_messages = self._convert_messages(messages)
        response = await self._llm.ainvoke(langchain_messages)
        return response.content

    async def generate_stream(self, messages: list[dict]):
        """스트리밍 응답 생성"""
        langchain_messages = self._convert_messages(messages)
        async for chunk in self._llm.astream(langchain_messages):
            if chunk.content:
                yield chunk.content

    def _convert_messages(self, messages: list[dict]) -> list:
        """OpenAI 포맷 → LangChain 메시지 포맷 변환"""
        langchain_messages = []
        for msg in messages:
            role = msg["role"]
            content = msg["content"]

            if role == "system":
                langchain_messages.append(SystemMessage(content=content))
            elif role == "user":
                langchain_messages.append(HumanMessage(content=content))
            elif role == "assistant":
                langchain_messages.append(AIMessage(content=content))

        return langchain_messages
