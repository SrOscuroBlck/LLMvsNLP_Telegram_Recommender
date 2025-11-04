class ChatbotError(Exception):
    pass


class ConfigurationError(ChatbotError):
    pass


class CorpusEmptyError(ChatbotError):
    pass


class InvalidQueryError(ChatbotError):
    pass


class OpenAIError(ChatbotError):
    pass


class TelegramError(ChatbotError):
    pass
