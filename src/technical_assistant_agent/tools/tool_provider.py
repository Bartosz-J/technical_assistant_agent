from abc import ABC, abstractmethod
from typing import Any

from technical_assistant_agent.models.tool import Tool
from technical_assistant_agent.models.tool_call import ToolCall
from technical_assistant_agent.models.agent_context import AgentContext
from technical_assistant_agent.models.tool_result import ToolResult

# abstrakcja, jakby nam przyszlo do glowy jednak nie robic po MCP...
class ToolProvider(ABC):

    @abstractmethod
    async def list_tools(self) -> list[Tool]:
        raise NotImplementedError

    @abstractmethod
    async def call_tool(
        self,
        #name: str,
        tool_call: ToolCall, #dict[str, Any]
        agent_context: AgentContext # bo czesc informacji jak user_id i machine_id bedzie stad
    ) -> ToolResult:
        raise NotImplementedError