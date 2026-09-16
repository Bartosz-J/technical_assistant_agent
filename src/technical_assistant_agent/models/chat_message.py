from pydantic import BaseModel, Field
from technical_assistant_agent.models.tool_call import ToolCall
from technical_assistant_agent.models.tool import Tool
from typing import Any, Literal

UserRole = Literal[
    "system",
    "user",
    "assistant",
    "tool"
]

class ChatMessage(BaseModel):
    role: UserRole
    content: str | None = None          # moze byc None, bo odpowiedz moze zawierac tylko ToolCalla
    # tool_call_id: str | None = None
    #tool_call: ToolCall | None = None

    tool_calls: list[ToolCall] = Field(default_factory = list)  # lista, bo w jednej odpowiedzi z ollamy moze byc kilka tool calli!

    #tool_name: str | None = None
