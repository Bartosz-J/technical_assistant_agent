from pydantic import BaseModel
# from technical_assistant_agent.models.agent_context import AgentContext
from technical_assistant_agent.models.chat_history import ChatHistory
from technical_assistant_agent.models.agent_stop_reason import AgentStopReason

class AgentState(BaseModel):

    user_message: str

    chat_history: ChatHistory

    iteration: int = 0
    tool_calls: int = 0

    finished: bool = False

    final_answer: str | None = None
    stop_reason: AgentStopReason | None = None