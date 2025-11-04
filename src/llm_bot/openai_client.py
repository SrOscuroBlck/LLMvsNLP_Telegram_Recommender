from pathlib import Path
from typing import List

from openai import OpenAI

from src.common.config import LLMBotConfig
from src.common.exceptions import OpenAIError
from src.common.logger import get_logger

logger = get_logger(__name__)


class OpenAIClient:
    def __init__(self, config: LLMBotConfig):
        self.config = config
        self.client = OpenAI(api_key=config.openai_api_key)
        logger.info(f"OpenAI Client initialized with model {config.model}")
    
    async def get_completion(self, messages: List[dict]) -> str:
        try:
            formatted_input = []
            for msg in messages:
                if msg["role"] == "system":
                    formatted_input.insert(0, {
                        "role": "user",
                        "content": f"[System Instructions: {msg['content']}]"
                    })
                else:
                    formatted_input.append({
                        "role": msg["role"],
                        "content": msg["content"]
                    })
            
            response = self.client.responses.create(
                model=self.config.model,
                input=formatted_input
            )
            
            answer = response.output_text
            logger.debug(f"OpenAI response received")
            return answer
            
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise OpenAIError(f"Failed to get completion from OpenAI: {e}")


def load_system_prompt(file_path: Path) -> str:
    if not file_path.exists():
        raise FileNotFoundError(f"System prompt file not found: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        prompt = f.read().strip()
    
    logger.info(f"Loaded system prompt from {file_path}")
    return prompt
