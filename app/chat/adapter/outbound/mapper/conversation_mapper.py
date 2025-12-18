from app.chat.adapter.outbound.entity import ConversationDocument
from app.chat.domain.entity import Conversation


class ConversationMapper:
    @staticmethod
    def to_domain(doc: ConversationDocument) -> Conversation:
        """
        ConversationDocument → Domain Conversation
        """
        return Conversation(
            id=doc.id,
            user_id=doc.user_id,
            character_id=doc.character_id,
            summary=doc.summary,
            last_message=doc.last_message,
            last_message_at=doc.last_message_at,
            created_at=doc.created_at,
            updated_at=doc.updated_at,
            language=doc.language,
            conversation_type=doc.conversation_type,
        )

    @staticmethod
    def to_document(domain: Conversation) -> ConversationDocument:
        """
        Domain Conversation → ConversationDocument
        """
        return ConversationDocument(
            id=domain.id,
            user_id=domain.user_id,
            character_id=domain.character_id,
            summary=domain.summary,
            last_message=domain.last_message,
            last_message_at=domain.last_message_at,
            language=domain.language,
            conversation_type=domain.conversation_type,
            created_at=domain.created_at,
            updated_at=domain.updated_at,
        )
