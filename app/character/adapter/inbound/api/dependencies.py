# Application Layer
from app.character.application.usecase import GetPersonasUseCase


# UseCase Factories
def get_personas_usecase() -> GetPersonasUseCase:
    return GetPersonasUseCase()
