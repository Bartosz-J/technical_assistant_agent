from pydantic import BaseModel, Field
from technical_assistant_agent.models.chat_message import ChatMessage

class ChatHistory(BaseModel):
    messsages: list[ChatMessage] = Field(default_factory = list)

    def add(
        self,
        message: ChatMessage
    ) -> None:
        self.messsages.append(message)

    def clear(
        self
    ) -> None:
        self.messsages.clear()