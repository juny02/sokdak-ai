from app.character.adapter.outbound.entity import CharacterDocument
from app.character.domain.entity import Character
from app.character.domain.enum import (
    CharacterType,
    Gender,
    Purpose,
    Style,
    Tone,
)
from app.character.domain.valueobject import Persona


class CharacterMapper:
    @staticmethod
    def to_domain(doc: CharacterDocument) -> Character:
        """
        CharacterDocument → Domain Character
        """
        return Character(
            id=doc.id,
            user_id=doc.user_id,
            name=doc.name,
            persona=Persona(
                gender=Gender(doc.persona["gender"]),
                tone=Tone(doc.persona["tone"]),
                style=Style(doc.persona["style"]),
                purpose=Purpose(doc.persona["purpose"]),
            ),
            type=CharacterType(doc.type),
            last_chat_at=doc.last_chat_at,
            created_at=doc.created_at,
            updated_at=doc.updated_at,
        )

    @staticmethod
    def to_document(character: Character) -> CharacterDocument:
        """
        Domain Character → CharacterDocument
        """
        return CharacterDocument(
            id=character.id,
            user_id=character.user_id,
            name=character.name,
            type=character.type,
            persona={
                "gender": character.persona.gender.value,
                "tone": character.persona.tone.value,
                "style": character.persona.style.value,
                "purpose": character.persona.purpose.value,
            },
            created_at=character.created_at,
            updated_at=character.updated_at,
            last_chat_at=character.last_chat_at,
        )
