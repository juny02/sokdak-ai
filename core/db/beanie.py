from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from app.character.adapter.outbound.entity import (
    CharacterDocument,
)
from app.chat.adapter.outbound.entity import ConversationDocument, MessageDocument

from ..setting import settings


async def init_db(client: AsyncIOMotorClient) -> None:
    await init_beanie(
        database=client[settings.MONGO_DB_NAME],
        document_models=[
            CharacterDocument,
            ConversationDocument,
            MessageDocument,
        ],
    )
