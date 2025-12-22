import pytest

from app.chat.domain.enum import ConversationType, Language


@pytest.mark.asyncio
async def test_post_message_uses_ephemeral_repo(
    client,
    ephemeral_message_repo,
    persistent_message_repo,
    conversation_factory,
    character_factory,
):
    """
    GIVEN: EPHEMERAL 대화가 존재할 때
    WHEN: 메시지 전송 API를 호출하면
    THEN: 200 OK와 AI 응답이 반환되고 ephemeral message repo가 사용된다
    """

    # GIVEN
    character = character_factory()
    conversation = conversation_factory(
        character_id=character.id,
        conversation_type=ConversationType.EPHEMERAL,
        language=Language.KOREAN,
    )

    # WHEN
    res = await client.post(
        f"/conversations/{conversation.id}/messages",
        json={"content": "안녕"},
    )

    # THEN
    assert res.status_code == 200
    body = res.json()
    assert body["role"] == "ai"
    assert body["content"] is not None

    assert ephemeral_message_repo._is_called is True
    assert persistent_message_repo._is_called is False


@pytest.mark.asyncio
async def test_post_message_uses_persistent_repo(
    client,
    ephemeral_message_repo,
    persistent_message_repo,
    conversation_factory,
    character_factory,
):
    """
    GIVEN: PERSISTENT 대화가 존재할 때
    WHEN: 메시지 전송 API를 호출하면
    THEN: 200 OK와 AI 응답이 반환되고 persistent message repo가 사용된다
    """

    # GIVEN
    character = character_factory()
    conversation = conversation_factory(
        character_id=character.id,
        conversation_type=ConversationType.PERSISTENT,
        language=Language.KOREAN,
    )

    # WHEN
    res = await client.post(
        f"/conversations/{conversation.id}/messages",
        json={"content": "오늘 하루 어땠어?"},
    )

    # THEN
    assert res.status_code == 200
    body = res.json()
    assert body["role"] == "ai"
    assert body["content"] is not None

    assert persistent_message_repo._is_called is True
    assert ephemeral_message_repo._is_called is False
