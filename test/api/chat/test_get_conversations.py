import pytest


@pytest.mark.asyncio
async def test_get_conversations_success(client):
    """
    GIVEN: 대화가 존재하지 않거나 여러 개 존재할 수 있을 때
    WHEN: GET /conversations 요청을 보내면
    THEN: 200 OK 와 함께 대화 목록(items)이 반환된다
    """

    # WHEN: 대화 목록 조회 요청
    res = await client.get("/conversations")

    # THEN: 정상 응답
    assert res.status_code == 200

    body = res.json()

    # AND: 응답에 items 필드가 존재하고 리스트 타입이다
    assert "items" in body
    assert isinstance(body["items"], list)
