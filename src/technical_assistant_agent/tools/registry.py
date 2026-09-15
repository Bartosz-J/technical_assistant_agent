from technical_assistant_agent.models.tool import Tool

class ToolRegistry:

    # ten rejestr po to, zeby agent nawet nie wiedzial czy korzysta z MCP
    # moze tereaz troche na wyrost, ale przyda sie jak bedziemy mieli osobne MCP dla historii eksploatacji
    # moze wtedy 2 x MCP ale tylko 1 x ToolRegistry?
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

    def add_tools(
        self,
        tools: list[Tool]
    ) -> None:

        for tool in tools:
            self.tools[tool.name] = tool