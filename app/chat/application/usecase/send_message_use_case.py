import asyncio
import time

from app.character.application.error import CharacterNotFoundError
from app.character.domain.repository import CharacterRepository
from app.chat.application.command import SendMessageCommand
from app.chat.application.error import ConversationNotFoundError
from app.chat.domain.entity import Message
from app.chat.domain.enum import Role
from app.chat.domain.repository import ConversationRepository, MessageRepository
from core.ai.service import LLMService
from core.logging import get_logger

logger = get_logger("latency")


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

    async def _update_summary(
        self,
        conversation,
        messages: list[Message],
        saved_ai_message: Message,
    ) -> None:
        """백그라운드에서 대화 요약을 업데이트합니다. 실패해도 채팅 응답에 영향 없음."""
        t_start = time.perf_counter()
        try:
            summary_response = await self.llm_service.summarize(
                previous_summary=conversation.summary,
                # TODO: 추후 설정값으로 변경
                recent_messages=messages[-9:] + [saved_ai_message],
            )
            conversation.update_last_message(saved_ai_message.content)
            conversation.update_summary(summary_response)
            await self.conversation_repo.update(conversation)
            elapsed = (time.perf_counter() - t_start) * 1000
            logger.info(f"[LATENCY] STEP7(bg) summarize + update: {elapsed:.1f}ms")
        except Exception as e:
            logger.error(f"[LATENCY] STEP7(bg) summarize failed: {e}")

    async def __call__(self, cmd: SendMessageCommand) -> Message:
        """
        메시지를 전송하고 AI 응답을 반환합니다.
        """
        t0 = time.perf_counter()

        # 1) 유저 메시지 저장
        await self.message_repo.create(
            conversation_id=cmd.conversation_id,
            content=cmd.content,
            role=Role.USER,
        )
        t1 = time.perf_counter()
        logger.info(
            f"[LATENCY] STEP1 message_repo.create(user): {(t1 - t0) * 1000:.1f}ms"
        )

        # 2) 최근 메시지 조회
        messages = await self.message_repo.get(
            conversation_id=cmd.conversation_id,
            limit=10,  # TODO: 추후 설정값으로 변경
            before=None,
        )
        t2 = time.perf_counter()
        logger.info(f"[LATENCY] STEP2 message_repo.get(10): {(t2 - t1) * 1000:.1f}ms")

        # 3) 대화 조회
        conversation = await self.conversation_repo.get_by_id(id=cmd.conversation_id)
        if not conversation:
            raise ConversationNotFoundError()
        t3 = time.perf_counter()
        logger.info(f"[LATENCY] STEP3 conversation_repo.get: {(t3 - t2) * 1000:.1f}ms")

        # 4) 캐릭터 페르소나 조회
        character = await self.character_repo.get_by_id(id=conversation.character_id)
        if not character:
            raise CharacterNotFoundError()
        t4 = time.perf_counter()
        logger.info(f"[LATENCY] STEP4 character_repo.get: {(t4 - t3) * 1000:.1f}ms")

        # 5) AI 응답 생성
        chat_response = await self.llm_service.chat(
            persona=character.persona,
            summary=conversation.summary,
            history=messages,
            user_input=cmd.content,
            language=conversation.language,
        )
        t5 = time.perf_counter()
        logger.info(f"[LATENCY] STEP5 llm_service.chat: {(t5 - t4) * 1000:.1f}ms")

        # 6) AI 메시지 저장
        saved_ai_message = await self.message_repo.create(
            conversation_id=cmd.conversation_id,
            content=chat_response,
            role=Role.AI,
        )
        t6 = time.perf_counter()
        logger.info(
            f"[LATENCY] STEP6 message_repo.create(ai): {(t6 - t5) * 1000:.1f}ms"
        )

        # 7) 요약 + DB 업데이트를 백그라운드로 분리 (응답 블로킹 없음)
        asyncio.create_task(
            self._update_summary(conversation, messages, saved_ai_message)
        )

        mongo_ms = (t1 - t0 + t2 - t1 + t3 - t2 + t4 - t3 + t6 - t5) * 1000
        chat_ms = (t5 - t4) * 1000
        total_ms = (t6 - t0) * 1000
        logger.info(
            f"[LATENCY] TOTAL(user-facing)={total_ms:.1f}ms | "
            f"MongoDB={mongo_ms:.1f}ms | "
            f"chat={chat_ms:.1f}ms"
        )

        return saved_ai_message
