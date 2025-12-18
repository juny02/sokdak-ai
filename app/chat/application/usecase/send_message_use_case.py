from app.character.domain.repository import CharacterRepository
from app.chat.application.command import SendMessageCommand
from app.chat.application.error import ConversationNotFoundError
from app.chat.domain.entity import Message
from app.chat.domain.enum import Role
from app.chat.domain.repository import ConversationRepository, MessageRepository
from core.ai.service import LLMService


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
        self,
        message_repo: MessageRepository,
        conversation_repo: ConversationRepository,
        character_repo: CharacterRepository,
        llm_service: LLMService,
    ):
        self.message_repo = message_repo
        self.conversation_repo = conversation_repo
        self.character_repo = character_repo
        self.llm_service = llm_service

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

        # 3) 대화 조회
        conversation = await self.conversation_repo.get_by_id(id=cmd.conversation_id)
        if not conversation:
            raise ConversationNotFoundError()

        # 4) 캐릭터 페르소나 조회
        character = await self.character_repo.get_by_id(id=conversation.character_id)

        # 5) AI 응답 생성
        chat_response = await self.llm_service.chat(
            persona=character.persona,
            summary=conversation.summary,
            history=messages,
            user_input=cmd.content,
            language=conversation.language,
        )

        # 6) AI 메시지 저장
        saved_ai_message = await self.message_repo.create(
            conversation_id=cmd.conversation_id,
            content=chat_response,
            role=Role.AI,
        )

        # 6) Conversation 업데이트 (요약 + 마지막 메시지)
        summary_response = await self.llm_service.summarize(
            previous_summary=conversation.summary,
            # TODO: 추후 설정값으로 변경
            recent_messages=messages[-9:] + [saved_ai_message],
        )
        conversation.update_last_message(saved_ai_message.content)
        conversation.update_summary(summary_response)
        await self.conversation_repo.update(conversation)

        return saved_ai_message
