from technical_assistant_agent.tools.tool_provider import ToolProvider
from technical_assistant_agent.models.tool_call import ToolCall

class ToolExecutor:

    def __init__(
        self,
        tool_provider: ToolProvider
    ) -> None:

        self.tool_provider = tool_provider

    async def execute(
        self,
        tool_call: ToolCall
    ):
        return await self.tool_provider.call_tool(
            tool_call = tool_call
        )