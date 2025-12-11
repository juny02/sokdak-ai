from app.chat.application.command import SendMessageCommand
from app.chat.domain.entity import Message
from app.chat.domain.enum import Role
from app.chat.domain.repository import ConversationRepository, MessageRepository


class SendMessageUseCase:
    """
    유저 메시지를 저장하고, 대화 맥락을 기반으로 AI 응답을 생성한 뒤
    대화의 마지막 메시지 및 요약을 업데이트합니다.
    AI 응답을 반환합니다.

    흐름:
        1) 유저 메시지 저장
        2) 최근 메시지 조회
        3) 대화 요약 조회
        4) 캐릭터 페르소나 조회
        5) 위 정보를 기반으로 프롬프트 생성 → AI 응답 생성
        6) AI 메시지 저장
        7) Conversation 요약 및 마지막 메시지 업데이트
    """

    def __init__(
        self, message_repo: MessageRepository, conversation_repo: ConversationRepository
    ):
        self.message_repo = message_repo
        self.conversation_repo = conversation_repo

    async def __call__(self, cmd: SendMessageCommand) -> Message:
        """
        메시지를 전송하고 AI 응답을 반환합니다.
        """
        # 1) 유저 메시지 저장
        await self.message_repo.create(
            conversation_id=cmd.conversation_id,
            content=cmd.content,
            role=Role.USER,
        )

        # 2) 최근 메시지 조회
        messages = await self.message_repo.get(
            conversation_id=cmd.conversation_id,
            limit=10,  # TODO: 추후 설정값으로 변경
            before=None,
        )
        # 3) 대화 요약 조회
        conversation = await self.conversation_repo.get_by_id(id=cmd.conversation_id)

        # 4) 캐릭터 페르소나 조회
        # TODO: 해당 conversation의 캐릭터 페르소나 조회
        persona = "This is a placeholder character persona."

        # 5) 프롬프트 생성 -> AI 응답 생성
        prompt = (
            f"Persona:\n{persona}\n\n"
            f"Conversation Summary:\n{conversation.summary}\n\n"
            f"Messages:\n{messages}\n\n"
        )
        # TODO: prompt 기반 AI 응답 생성
        ai_content = f"This is a placeholder AI response with prompt:\n{prompt}"

        # 6) AI 메시지 저장
        saved_ai_message = await self.message_repo.create(
            conversation_id=cmd.conversation_id,
            content=ai_content,
            role=Role.AI,
        )

        # 6) Conversation 업데이트 (요약 + 마지막 메시지)
        conversation.update_last_message(saved_ai_message.content)
        conversation.update_summary("This is an updated placeholder summary.")
        await self.conversation_repo.update(conversation)

        return saved_ai_message
