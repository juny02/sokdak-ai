import pytest
from ulid import ULID


@pytest.mark.asyncio
async def test_get_character_by_id_success(client, character_factory):
    """
    GIVEN: 캐릭터가 존재할 때
    WHEN: GET /characters/{id} 요청을 보내면
    THEN: 200 OK와 함께 해당 캐릭터 정보가 반환된다
    """

    # GIVEN
    character = character_factory()

    # WHEN
    res = await client.get(f"/characters/{character.id}")

    # THEN
    assert res.status_code == 200
    body = res.json()
    assert body["id"] == str(character.id)


@pytest.mark.asyncio
async def test_get_character_by_id_not_found(client):
    """
    GIVEN: 캐릭터가 존재하지 않을 때
    WHEN: GET /characters/{id} 요청을 보내면
    THEN: 404 Not Found가 반환된다
    """

    # WHEN
    res = await client.get(f"/characters/{ULID()}")

    # THEN
    assert res.status_code == 404
