from datetime import datetime, timezone

import pytest
from ulid import ULID

from app.character.domain.entity import Character
from app.character.domain.enum import Appearance, CharacterType, Purpose, Style, Tone
from app.character.domain.valueobject import Persona
from app.chat.adapter.inbound.api.dependencies import (
    get_character_repo,
    get_conversation_repo,
    get_ephemeral_message_repo,
    get_llm_service,
    get_persistent_message_repo,
)
from app.chat.domain.entity import Conversation
from app.chat.domain.enum import ConversationType, Language
from app.main import app
from core.ai.service import OpenAIService
from test.double.ai import FakeLLMClient
from test.double.repository import (
    InMemoryCharacterRepository,
    InMemoryConversationRepository,
    InMemoryEphemeralMessageRepository,
    InMemoryPersistentMessageRepository,
)

# ----------------------------
# Repository fixtures
# ----------------------------


@pytest.fixture
def character_repo():
    return InMemoryCharacterRepository()


@pytest.fixture
def conversation_repo():
    return InMemoryConversationRepository()


@pytest.fixture
def persistent_message_repo():
    return InMemoryPersistentMessageRepository()


@pytest.fixture
def ephemeral_message_repo():
    return InMemoryEphemeralMessageRepository()


# ----------------------------
# Dependency override (autouse)
# ----------------------------


@pytest.fixture(autouse=True)
def override_dependencies(
    character_repo,
    conversation_repo,
    persistent_message_repo,
    ephemeral_message_repo,
):
    """
    API 테스트 전용 dependency override
    - DB / Redis / OpenAI 전부 in-memory & fake로 대체
    """

    app.dependency_overrides[get_character_repo] = lambda: character_repo
    app.dependency_overrides[get_conversation_repo] = lambda: conversation_repo
    app.dependency_overrides[get_persistent_message_repo] = (
        lambda: persistent_message_repo
    )
    app.dependency_overrides[get_ephemeral_message_repo] = (
        lambda: ephemeral_message_repo
    )
    app.dependency_overrides[get_llm_service] = lambda: OpenAIService(FakeLLMClient())

    yield

    app.dependency_overrides.clear()


# ----------------------------
# Test data factories
# ----------------------------


@pytest.fixture
def conversation_factory(conversation_repo):
    """
    테스트용 Conversation 도메인 객체를 생성하고
    InMemoryConversationRepository에 저장하는 팩토리 픽스처.

    - 필요한 필드만 override 가능
    - 매 호출마다 새로운 Conversation을 생성
    - API / UseCase 테스트에서 공통으로 사용
    """

    def _create(
        *,
        id: ULID | None = None,
        user_id: ULID | None = None,
        character_id: ULID | None = None,
        summary: str | None = None,
        language: Language = Language.KOREAN,
        conversation_type: ConversationType = ConversationType.EPHEMERAL,
    ) -> Conversation:
        conversation = Conversation(
            id=id or ULID(),
            user_id=user_id or ULID(),
            character_id=character_id or ULID(),
            summary=summary,
            last_message=None,
            last_message_at=None,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
            language=language,
            conversation_type=conversation_type,
        )

        conversation_repo._store[conversation.id] = conversation
        return conversation

    return _create


@pytest.fixture
def character_factory(character_repo):
    """
    테스트용 Character 도메인 객체를 생성하고
    InMemoryCharacterRepository에 저장하는 팩토리 픽스처.

    - 필요한 필드만 override 가능
    - 매 호출마다 새로운 Character을 생성
    - API / UseCase 테스트에서 공통으로 사용
    """

    def _create(
        *,
        id: ULID | None = None,
        user_id: ULID | None = None,
        name: str = "Test Character",
        persona: Persona | None = None,
        appearance: Appearance = Appearance.FRIEND,
        type: CharacterType = CharacterType.PERSISTENT,
        last_chat_at=None,
    ) -> Character:
        now = datetime.now(timezone.utc)

        character = Character(
            id=id or ULID(),
            user_id=user_id or ULID(),
            name=name,
            persona=persona
            or Persona(
                tone=Tone.CALM,
                style=Style.LISTENER,
                purpose=Purpose.CONFESSION,
            ),
            appearance=appearance,
            type=type,
            last_chat_at=last_chat_at,
            created_at=now,
            updated_at=now,
        )

        character_repo._store[character.id] = character

        return character

    return _create
