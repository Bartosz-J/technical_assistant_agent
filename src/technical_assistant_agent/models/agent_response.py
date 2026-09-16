from pydantic import BaseModel

class AgentResponse(BaseModel):

    anwer: str

    #tool_calls: list

    iterations: int

    trace_id: str | None = None

    metadata: dict = {}