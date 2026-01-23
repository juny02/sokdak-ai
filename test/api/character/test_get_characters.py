import pytest
from ulid import ULID

from app.character.domain.enum import CharacterType


@pytest.mark.asyncio
async def test_get_characters_returns_items(client, character_factory):
    """
    GIVEN: 유저가 보유한 캐릭터가 존재할 때
    WHEN: GET /characters 요청을 보내면
    THEN: items 배열을 포함한 200 응답이 반환된다
    """

    # GIVEN
    user_id = ULID()
    character_factory(user_id=user_id)
    character_factory(user_id=user_id)

    # WHEN
    res = await client.get("/characters", params={"user_id": str(user_id)})

    # THEN
    assert res.status_code == 200
    body = res.json()
    assert "items" in body
    assert isinstance(body["items"], list)
    assert len(body["items"]) >= 2


@pytest.mark.asyncio
async def test_get_characters_filters_by_type(client, character_factory):
    """
    GIVEN: 서로 다른 type의 캐릭터가 존재할 때
    WHEN: GET /characters?type=... 요청을 보내면
    THEN: 해당 type 캐릭터만 반환된다
    """

    # GIVEN
    user_id = ULID()
    character_factory(user_id=user_id, type=CharacterType.PERSISTENT)
    character_factory(user_id=user_id, type=CharacterType.EPHEMERAL)

    # WHEN
    res = await client.get(
        "/characters",
        params={"user_id": str(user_id), "type": CharacterType.PERSISTENT.value},
    )

    # THEN
    assert res.status_code == 200
    body = res.json()
    items = body["items"]
    assert all(item["type"] == CharacterType.PERSISTENT.value for item in items)
