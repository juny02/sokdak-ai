import pytest


@pytest.mark.asyncio
async def test_patch_character_updates_name(client, character_factory):
    """
    GIVEN: 캐릭터가 존재할 때
    WHEN: PATCH /characters/{id} 로 name을 변경하면
    THEN: 200 OK와 함께 변경된 캐릭터가 반환된다
    """

    # GIVEN
    character = character_factory(name="원래이름")
    payload = {"name": "바뀐이름"}

    # WHEN
    res = await client.patch(f"/characters/{character.id}", json=payload)

    # THEN
    assert res.status_code == 200
    body = res.json()
    assert body["id"] == str(character.id)
    assert body["name"] == "바뀐이름"


@pytest.mark.asyncio
async def test_patch_character_not_found(client):
    """
    GIVEN: 캐릭터가 존재하지 않을 때
    WHEN: PATCH /characters/{id} 요청을 보내면
    THEN: 404 Not Found가 반환된다
    """

    # WHEN
    res = await client.patch(
        f"/characters/{'01JZZZZZZZZZZZZZZZZZZZZZZZ'}", json={"name": "x"}
    )

    # THEN
    assert res.status_code == 404
