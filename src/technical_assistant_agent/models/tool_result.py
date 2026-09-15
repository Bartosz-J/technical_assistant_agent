from pydantic import BaseModel
from typing import Any
#from uuid import UUID

class ToolResult(BaseModel):
    tool_call_id: str
    name: str
    content: str | None = None
    structured_content: Any | None = None
    is_error: bool = False
    # success: bool
    # data: object | None = None
    # error: str | None = None    # chcemy zeby tool zwracal bledy bez wywalenia calego agenta
    # metadata: dict = {}