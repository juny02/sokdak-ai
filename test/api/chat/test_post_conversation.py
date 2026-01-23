import pytest
from ulid import ULID


@pytest.mark.asyncio
async def test_post_conversation(client):
    """
    GIVEN: 유효한 대화 생성 요청 payload가 주어졌을 때
    WHEN: POST /conversations 요청을 보내면
    THEN: 201 Created 와 함께 생성된 conversation 정보가 반환된다
    """
    payload = {
        "character_id": str(ULID()),
        "user_id": str(ULID()),
        "language": "korean",
        "conversation_type": "ephemeral",
    }

    res = await client.post("/conversations", json=payload)

    assert res.status_code == 201

    body = res.json()
    assert body["id"] is not None
    assert body["character_id"] == payload["character_id"]
    assert body["user_id"] == payload["user_id"]
    assert body["language"] == payload["language"]
    assert body["conversation_type"] == payload["conversation_type"]
