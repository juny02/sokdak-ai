from typing import Literal, TypedDict


class OpenAIMessage(TypedDict):
    role: Literal["system", "user", "assistant"]
    content: str
