from enum import Enum


class Purpose(str, Enum):
    CONFESSION = "confession"
    COUNSELING = "counseling"
    EMOTIONAL_SUPPORT = "emotional_support"
    CASUAL_CHAT = "casual_chat"
    MOTIVATION = "motivation"
    REFLECTION = "reflection"
