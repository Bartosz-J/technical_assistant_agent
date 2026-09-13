from pydantic import BaseModel
from uuid import UUID

from technical_assistant_agent.models.tool_result import ToolResult

class ToolCall(BaseModel):
    id: UUID
    tool_name: str
    arguments: dict
    result: ToolResult
    duration_ms: int | None = None # ile zajelo wywolanie narzedzia?