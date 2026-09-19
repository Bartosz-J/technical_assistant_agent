from pydantic import BaseModel, Field

from technical_assistant_agent.models.chat_history import ChatHistory
from technical_assistant_agent.models.agent_context import AgentContext


class ChatCall(BaseModel):
    message: str

    agent_context: AgentContext = Field(
        default_factory = AgentContext
    )
    # user_id: str | None = None
    # machine_id: str | None = None

    chat_history: ChatHistory = Field(
        default_factory = ChatHistory
    )