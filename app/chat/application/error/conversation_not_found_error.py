class ConversationNotFoundError(Exception):
    def __init__(self, message="Conversation not found."):
        super().__init__(message)
