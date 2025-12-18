from motor.motor_asyncio import AsyncIOMotorClient

from ..setting import settings


class MongoClientFactory:
    """
    AsyncIOMotorClient 싱글톤 팩토리
    - 앱 전체에서 단 하나의 Mongo client만 유지
    - 연결 생성 / 재사용만 책임
    """

    _client: AsyncIOMotorClient | None = None

    @classmethod
    def get_client(cls) -> AsyncIOMotorClient:
        if cls._client is None:
            cls._client = AsyncIOMotorClient(
                settings.MONGO_URI,
            )
        return cls._client
