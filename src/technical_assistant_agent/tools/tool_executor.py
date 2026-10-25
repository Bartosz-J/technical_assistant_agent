from technical_assistant_agent.tools.tool_provider import ToolProvider
from technical_assistant_agent.models.agent_context import AgentContext
from technical_assistant_agent.models.tool_call import ToolCall
from technical_assistant_agent.models.tool_result import ToolResult

class ToolExecutor:

    def __init__(
        self,
        tool_provider: ToolProvider
    ) -> None:

        self.tool_provider = tool_provider

    async def execute(
        self,
        tool_call: ToolCall,
        agent_context: AgentContext
    ) -> ToolResult:

        print("wywolujemy narzerzie:")
        print(tool_call)
        
        return await self.tool_provider.call_tool(
            tool_call = tool_call,
            agent_context = agent_context
        )