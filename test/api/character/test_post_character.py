import pytest
from ulid import ULID


@pytest.mark.asyncio
async def test_post_character_creates_character(client):
    """
    GIVEN: 유효한 캐릭터 생성 요청이 있을 때
    WHEN: POST /characters 요청을 보내면
    THEN: 201 Created와 함께 생성된 캐릭터가 반환된다
    """

    # GIVEN
    payload = {
        "user_id": str(ULID()),
        "name": "테스트 캐릭터",
        "persona": {
            "tone": "calm",
            "style": "listener",
            "purpose": "confession",
        },
        "appearance": "friend",
        "type": "persistent",
    }

    # WHEN
    res = await client.post("/characters", json=payload)

    # THEN
    assert res.status_code == 201
    body = res.json()

    assert body["id"] is not None
    assert body["user_id"] == payload["user_id"]
    assert body["name"] == payload["name"]
    assert body["type"] == payload["type"]

    assert body["persona"]["tone"] == payload["persona"]["tone"]
    assert body["persona"]["style"] == payload["persona"]["style"]
    assert body["persona"]["purpose"] == payload["persona"]["purpose"]
    assert body["appearance"] == payload["appearance"]
