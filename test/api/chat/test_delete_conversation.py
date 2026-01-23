import pytest
from ulid import ULID

from app.chat.domain.enum import ConversationType, Language


@pytest.mark.asyncio
async def test_delete_conversation_success(client, conversation_factory):
    """
    GIVEN: conversation이 존재할 때
    WHEN: DELETE /conversations/{conversation_id} 요청을 보내면
    THEN: 204 No Content 를 반환한다
    """

    # GIVEN: 테스트용 conversation 하나를 미리 생성한다
    conversation = conversation_factory(
        language=Language.KOREAN,
        conversation_type=ConversationType.EPHEMERAL,
    )
    conversation_id = conversation.id

    # WHEN: DELETE API 호출
    res = await client.delete(f"/conversations/{conversation_id}")

    # THEN: 성공적으로 삭제되었음을 상태 코드로 확인한다
    assert res.status_code == 204


@pytest.mark.asyncio
async def test_delete_conversation_not_found(client):
    """
    GIVEN: conversation이 존재하지 않을 때
    WHEN: DELETE /conversations/{conversation_id} 요청을 보내면
    THEN: 404 Not Found 를 반환한다
    """
    conversation_id = str(ULID())

    res = await client.delete(f"/conversations/{conversation_id}")

    assert res.status_code == 404
