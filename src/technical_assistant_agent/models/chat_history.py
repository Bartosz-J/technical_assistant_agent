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

    # uzytkownikowi chcemy zwracac tylko historie konwersacji, bez system_promptu!
    # moze rowniez bez konkretnych tool_calli? Do przemyslenia...
    def public(
        self
    ):
        public_messages = [
            message 
            for message in self.messages
            if message.role != "system"
        ]

        return ChatHistory(
            messages = public_messages
        )