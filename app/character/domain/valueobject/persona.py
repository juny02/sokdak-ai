from enum import Enum
from dataclasses import dataclass

class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    NEUTRAL = "neutral"


class Tone(str, Enum):
    CALM = "calm"
    WARM = "warm"
    CHEERFUL = "cheerful"
    SERIOUS = "serious"
    FRIENDLY = "friendly"
    POLITE = "polite"
    PLAYFUL = "playful"


class Style(str, Enum):
    LISTENER = "listener"
    EMPATHETIC = "empathetic"
    ADVISOR = "advisor"
    COACH = "coach"
    CHATTY = "chatty"
    MINIMAL = "minimal"
    ANALYTICAL = "analytical"


class Purpose(str, Enum):
    CONFESSION = "confession"
    COUNSELING = "counseling"
    EMOTIONAL_SUPPORT = "emotional_support"
    CASUAL_CHAT = "casual_chat"
    MOTIVATION = "motivation"
    REFLECTION = "reflection"


@dataclass(frozen=True)
class Persona:
    gender: Gender
    tone: Tone
    style: Style
    purpose: Purpose
