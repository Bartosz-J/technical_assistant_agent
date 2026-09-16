from pydantic import BaseModel, Field
from technical_assistant_agent.models.chat_message import ChatMessage

class ChatHistory(BaseModel):
    messages: list[ChatMessage] = Field(default_factory = list)

    def add(
        self,
        message: ChatMessage
    ) -> None:
        self.messages.append(message)

    def clear(
        self
    ) -> None:
        self.messages.clear()