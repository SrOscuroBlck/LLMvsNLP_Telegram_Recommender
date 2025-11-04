import os
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv

from src.common.exceptions import ConfigurationError


@dataclass
class BotConfig:
    token: str
    log_level: str = "INFO"


@dataclass
class NLPBotConfig(BotConfig):
    similarity_threshold: float = 0.3


@dataclass
class LLMBotConfig(BotConfig):
    openai_api_key: str = ""
    model: str = ""
    temperature: float = 0.7
    max_tokens: int = 500
    max_conversation_history: int = 10


def load_environment() -> None:
    env_path = Path(__file__).parent.parent.parent / ".env"
    if env_path.exists():
        load_dotenv(env_path)


def validate_environment_variable(var_name: str) -> str:
    value = os.getenv(var_name)
    if not value:
        raise ConfigurationError(
            f"{var_name} environment variable is required but not set"
        )
    return value


def load_nlp_bot_config() -> NLPBotConfig:
    load_environment()
    
    token = validate_environment_variable("NLP_BOT_TOKEN")
    log_level = os.getenv("LOG_LEVEL", "INFO")
    similarity_threshold = float(os.getenv("SIMILARITY_THRESHOLD", "0.3"))
    
    return NLPBotConfig(
        token=token,
        log_level=log_level,
        similarity_threshold=similarity_threshold
    )


def load_llm_bot_config() -> LLMBotConfig:
    load_environment()
    
    token = validate_environment_variable("LLM_BOT_TOKEN")
    openai_api_key = validate_environment_variable("OPENAI_API_KEY")
    model = validate_environment_variable("OPENAI_MODEL")
    log_level = os.getenv("LOG_LEVEL", "INFO")
    temperature = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))
    max_tokens = int(os.getenv("OPENAI_MAX_TOKENS", "500"))
    max_history = int(os.getenv("MAX_CONVERSATION_HISTORY", "10"))
    
    return LLMBotConfig(
        token=token,
        openai_api_key=openai_api_key,
        log_level=log_level,
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        max_conversation_history=max_history
    )
