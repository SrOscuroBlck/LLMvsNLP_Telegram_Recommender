from dataclasses import dataclass, field
from typing import Dict, List

from src.common.logger import get_logger

logger = get_logger(__name__)


@dataclass
class Message:
    role: str
    content: str


@dataclass
class Conversation:
    messages: List[Message] = field(default_factory=list)
    
    def add_message(self, role: str, content: str):
        self.messages.append(Message(role=role, content=content))
    
    def get_messages_as_dicts(self) -> List[dict]:
        return [{"role": msg.role, "content": msg.content} for msg in self.messages]
    
    def get_message_count(self) -> int:
        return len(self.messages)
    
    def clear(self):
        self.messages.clear()


class ConversationManager:
    def __init__(self, max_history: int = 10):
        self.max_history = max_history
        self.conversations: Dict[int, Conversation] = {}
        logger.info(f"Conversation Manager initialized with max_history={max_history}")
    
    def get_conversation(self, user_id: int) -> Conversation:
        if user_id not in self.conversations:
            self.conversations[user_id] = Conversation()
            logger.info(f"Created new conversation for user {user_id}")
        return self.conversations[user_id]
    
    def add_user_message(self, user_id: int, content: str):
        conversation = self.get_conversation(user_id)
        conversation.add_message("user", content)
        self.trim_conversation(user_id)
        logger.debug(f"Added user message for user {user_id}")
    
    def add_assistant_message(self, user_id: int, content: str):
        conversation = self.get_conversation(user_id)
        conversation.add_message("assistant", content)
        logger.debug(f"Added assistant message for user {user_id}")
    
    def trim_conversation(self, user_id: int):
        conversation = self.get_conversation(user_id)
        
        if conversation.get_message_count() > self.max_history:
            messages_to_keep = conversation.messages[-self.max_history:]
            conversation.messages = messages_to_keep
            logger.debug(f"Trimmed conversation for user {user_id} to {self.max_history} messages")
    
    def get_messages_for_api(self, user_id: int, system_prompt: str) -> List[dict]:
        conversation = self.get_conversation(user_id)
        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(conversation.get_messages_as_dicts())
        return messages
    
    def reset_conversation(self, user_id: int):
        if user_id in self.conversations:
            self.conversations[user_id].clear()
            logger.info(f"Reset conversation for user {user_id}")
    
    def get_active_conversations_count(self) -> int:
        return len(self.conversations)
