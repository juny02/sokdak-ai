class CharacterNotFoundError(Exception):
    def __init__(self, message="Character not found."):
        super().__init__(message)
