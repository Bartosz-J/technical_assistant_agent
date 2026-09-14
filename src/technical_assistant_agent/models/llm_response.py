from pydantic import BaseModel
from technical_assistant_agent.models.chat_message import ChatMessage

class LLMResponse(BaseModel):
    message: ChatMessage
    finish_reason: str | None = None