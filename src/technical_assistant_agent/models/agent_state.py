from pydantic import BaseModel
from technical_assistant_agent.models.agent_context import AgentContext

class AgentState(BaseModel):

    user_message: str

    context: AgentContext

    iteration: int = 0
    tool_calls: int = 0

    finished: bool = False

    final_answer: str | None = None