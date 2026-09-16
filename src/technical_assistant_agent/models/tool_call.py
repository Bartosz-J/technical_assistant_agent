from pydantic import BaseModel
from typing import Any
from uuid import UUID

from technical_assistant_agent.models.tool_result import ToolResult

class ToolCall(BaseModel):
    id: str #UUID
    tool_name: str
    arguments: dict[str, Any]
    result: ToolResult | None = None
    duration_ms: int | None = None # ile zajelo wywolanie narzedzia?