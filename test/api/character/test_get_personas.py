import pytest


@pytest.mark.asyncio
async def test_get_personas_returns_all_categories(client):
    """
    GIVEN: 페르소나 키워드가 정의되어 있을 때
    WHEN: GET /characters/personas 요청을 보내면
    THEN: 각 카테고리(gender/tone/style/purpose) 배열을 포함한 200 응답이 반환된다
    """

    # WHEN
    res = await client.get("/characters/personas")

    # THEN
    assert res.status_code == 200
    body = res.json()

    assert "gender" in body and isinstance(body["gender"], list)
    assert "tone" in body and isinstance(body["tone"], list)
    assert "style" in body and isinstance(body["style"], list)
    assert "purpose" in body and isinstance(body["purpose"], list)
