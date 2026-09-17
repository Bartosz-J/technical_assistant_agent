from pydantic import BaseModel
from technical_assistant_agent.models.agent_stop_reason import AgentStopReason

class AgentResponse(BaseModel):

    answer: str

    #tool_calls: list

    iterations: int

    stop_reason: AgentStopReason

    trace_id: str | None = None

    metadata: dict = {}