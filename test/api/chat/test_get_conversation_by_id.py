import pytest
from ulid import ULID

from app.chat.domain.enum import ConversationType, Language


@pytest.mark.asyncio
async def test_get_conversation_by_id_success(client, conversation_factory):
    """
    GIVEN: 대화가 존재할 때
    WHEN: GET /conversations/{conversation_id} 요청을 보내면
    THEN: 200 OK 와 함께 해당 대화 정보가 반환된다
    """

    # GIVEN: 테스트용 conversation 하나를 미리 생성해 둔다
    conversation = conversation_factory(
        language=Language.KOREAN,
        conversation_type=ConversationType.EPHEMERAL,
    )

    # WHEN: 해당 대화 ID로 조회 요청
    res = await client.get(f"/conversations/{conversation.id}")

    # THEN: 정상 응답
    assert res.status_code == 200

    body = res.json()
    assert body["id"] == str(conversation.id)
    assert body["language"] == Language.KOREAN.value
    assert body["conversation_type"] == ConversationType.EPHEMERAL.value


@pytest.mark.asyncio
async def test_get_conversation_by_id_not_found(client):
    """
    GIVEN: 대화가 존재하지 않을 때
    WHEN: GET /conversations/{conversation_id} 요청을 보내면
    THEN: 404 Not Found 가 반환된다
    """

    # GIVEN: 존재하지 않는 ID
    non_existent_id = ULID()

    # WHEN: 조회 요청
    res = await client.get(f"/conversations/{non_existent_id}")

    # THEN: 404 응답
    assert res.status_code == 404

    body = res.json()
    assert body["message"] == "Conversation not found."
