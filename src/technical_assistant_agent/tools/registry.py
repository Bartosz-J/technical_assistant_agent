from technical_assistant_agent.models.tool import Tool

class ToolRegistry:

    def __init__(
        self,
        tools: list[Tool] | None = None
    ):
        self.tools: dict[str, Tool] = {
            tool.name: tool 
            for tool in (tools or [])
        }    

    def list_tools(self) -> list[Tool]:
        return list(self.tools.values())