from pydantic import BaseModel

class ToolResult(BaseModel):

    success: bool
    data: object | None = None
    error: str | None = None    # chcemy zeby tool zwracal bledy bez wywalenia calego agenta
    metadata: dict = {}