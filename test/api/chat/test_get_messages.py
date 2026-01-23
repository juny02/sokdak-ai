import pytest


@pytest.mark.asyncio
async def test_get_messages_success(client, conversation_factory):
    """
    GIVEN: conversation이 존재할 때
    WHEN: GET /conversations/{conversation_id}/messages 요청을 보내면
    THEN: 200 OK 와 함께 메시지 목록(items)이 반환된다
    """

    # GIVEN: 테스트용 conversation 하나를 미리 생성한다
    conversation = conversation_factory()

    # WHEN: 해당 conversation의 메시지 목록 조회
    res = await client.get(f"/conversations/{conversation.id}/messages")

    # THEN: 정상 응답
    assert res.status_code == 200

    body = res.json()

    # AND: items 필드가 존재하고 리스트 타입이다
    assert "items" in body
    assert isinstance(body["items"], list)


@pytest.mark.asyncio
async def test_get_messages_with_limit(client, conversation_factory):
    """
    GIVEN: conversation이 존재할 때
    WHEN: GET /conversations/{conversation_id}/messages 요청에 limit 파라미터를 주면
    THEN: 200 OK 와 함께 메시지 목록이 반환된다
    """

    # GIVEN: 테스트용 conversation 하나를 미리 생성한다
    conversation = conversation_factory()

    # WHEN: limit 파라미터를 포함하여 메시지 조회
    res = await client.get(
        f"/conversations/{conversation.id}/messages",
        params={"limit": 5},
    )

    # THEN: 정상 응답
    assert res.status_code == 200

    body = res.json()

    # AND: items 필드가 존재하고 리스트 타입이다
    assert "items" in body
    assert isinstance(body["items"], list)
