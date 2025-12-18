from datetime import datetime, timezone

from ulid import ULID

from app.character.adapter.outbound.entity.character_document import CharacterDocument
from app.character.adapter.outbound.mapper.character_mapper import CharacterMapper
from app.character.application.command import OrderBy
from app.character.domain.entity import Character
from app.character.domain.enum import CharacterType
from app.character.domain.repository import CharacterRepository
from app.character.domain.valueobject import Persona


class CharacterDocumentRepository(CharacterRepository):
    """
    MongoDB/Beanie 구현체
    - CharacterDocument를 직접 사용 (Beanie 전역 컨텍스트 사용)
    """

    async def get(
        self,
        user_id: ULID | None = None,
        order_by: OrderBy = OrderBy.CURR,
        type: CharacterType | None = None,
    ) -> list[Character]:
        """
        조건에 맞는 Character 목록 조회
        """

        conditions = []

        if user_id is not None:
            conditions.append(CharacterDocument.user_id == user_id)

        if type is not None:
            conditions.append(CharacterDocument.type == type)

        query = CharacterDocument.find(*conditions)

        sort_mapping: dict[OrderBy, str] = {
            OrderBy.CURR: "-created_at",  # 최신 생성순 (default)
            OrderBy.ASC: "created_at",  # 오래된 생성순
            OrderBy.DESC: "-last_chat_at",  # 최근 대화순
        }

        query = query.sort(sort_mapping[order_by])

        docs = await query.to_list()
        return [CharacterMapper.to_domain(doc) for doc in docs]

    async def get_by_id(self, id: ULID) -> Character | None:
        """
        ID로 단일 Character 조회
        """
        doc = await CharacterDocument.get(id)
        return CharacterMapper.to_domain(doc) if doc else None

    async def create(
        self,
        user_id: ULID,
        name: str,
        persona: Persona,
        type: CharacterType,
    ) -> Character:
        """
        새 Character 생성
        """
        now = datetime.now(timezone.utc)

        character = Character(
            id=ULID(),
            user_id=user_id,
            name=name,
            persona=persona,
            type=type,
            last_chat_at=None,
            created_at=now,
            updated_at=now,
        )

        doc = CharacterMapper.to_document(character)
        await doc.insert()

        return character

    async def update(self, character: Character) -> Character:
        """
        기존 Character 업데이트
        """
        # 1. 기존 Document 조회
        doc = await CharacterDocument.get(character.id)
        if not doc:
            raise ValueError(f"Character {character.id} not found")

        # 2. 필드 업데이트
        doc.name = character.name
        doc.type = character.type
        doc.persona = {
            "gender": character.persona.gender.value,
            "tone": character.persona.tone.value,
            "style": character.persona.style.value,
            "purpose": character.persona.purpose.value,
        }
        doc.last_chat_at = character.last_chat_at
        doc.updated_at = datetime.now(timezone.utc)

        # 3. 저장
        await doc.save()

        return CharacterMapper.to_domain(doc)

    async def delete_by_id(self, id: ULID) -> None:
        """
        Character 삭제
        """
        doc = await CharacterDocument.get(id)
        if doc:
            await doc.delete()
