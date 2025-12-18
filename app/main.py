from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.character.adapter.inbound.api.router import router as character_router
from app.chat.adapter.inbound.api.router import router as chat_router
from core.db import MongoClientFactory, init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. 싱글톤 MongoDB client 생성
    client = MongoClientFactory.get_client()

    # 2. Beanie 초기화
    await init_db(client)

    yield  # 애플리케이션 실행 중

    # Shutdown (선택사항)
    # MongoDB client 종료
    if MongoClientFactory._client:
        MongoClientFactory._client.close()
        MongoClientFactory._client = None


app = FastAPI(title="Sokdak AI API", version="0.1.0", lifespan=lifespan)
app.include_router(chat_router)
app.include_router(character_router)
