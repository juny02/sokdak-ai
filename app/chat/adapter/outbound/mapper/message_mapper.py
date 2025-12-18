from app.chat.adapter.outbound.entity import MessageDocument
from app.chat.domain.entity import Message


class MessageMapper:
    @staticmethod
    def to_domain(doc: MessageDocument) -> Message:
        """
        MessageDocument → Domain Message
        """
        return Message(
            id=doc.id,
            conversation_id=doc.conversation_id,
            role=doc.role,
            content=doc.content,
            created_at=doc.created_at,
        )

    @staticmethod
    def to_document(domain: Message) -> MessageDocument:
        """
        Domain Message → MessageDocument
        """
        return MessageDocument(
            id=domain.id,
            conversation_id=domain.conversation_id,
            role=domain.role,
            content=domain.content,
            created_at=domain.created_at,
        )
