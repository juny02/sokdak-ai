from ulid import ULID


def conversation_messages_key(conversation_id: ULID) -> str:
    """
    1회용(Ephemeral) 대화의 메시지 목록을 저장하는 Redis LIST 키를 생성한다.

    - Redis 자료구조: LIST
    - Key 형식: conversation:messages:{conversation_id}
    - 대화 하나당 하나의 LIST를 사용한다.
    - TTL은 Conversation 생성 시 설정되며, 만료 시 메시지 전체가 삭제된다.
    """
    return f"conversation:messages:{conversation_id}"
