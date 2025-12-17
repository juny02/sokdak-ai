from app.chat.domain.entity import Message
from app.chat.domain.enum import Role

from .message import OpenAIMessage


class OpenAIMessageFactory:
    @staticmethod
    def system(text: str) -> OpenAIMessage:
        return {"role": "system", "content": text}

    @staticmethod
    def user(text: str) -> OpenAIMessage:
        return {"role": "user", "content": text}

    @staticmethod
    def assistant(text: str) -> OpenAIMessage:
        return {"role": "assistant", "content": text}

    @staticmethod
    def from_domain(msg: Message) -> OpenAIMessage:
        if msg.role == Role.AI:
            return {"role": "assistant", "content": msg.content}
        elif msg.role == Role.USER:
            return {"role": "user", "content": msg.content}
        else:  # TODO: 예외처리
            return {"role": msg.role, "content": msg.content}
