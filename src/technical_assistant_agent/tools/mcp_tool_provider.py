from mcp import Client
from technical_assistant_agent.tools.tool_provider import ToolProvider
from technical_assistant_agent.models.tool import Tool
from technical_assistant_agent.models.tool_call import ToolCall
from technical_assistant_agent.models.tool_result import ToolResult

from typing import Any

class MCPToolProvider(ToolProvider):

    def __init__(
        self,
        mcp_server_url: str
    ) -> None:

        self.client = Client(
            server = mcp_server_url
        )

    async def list_tools(
        self
    ) -> list[Tool]:
        
        # sprawdzamy dostepne narzedzia:
        # async with self.client:
        #     result = await self.client.list_tools()
            
        #     tools = [
        #         Tool(
        #             name = tool.name,
        #             description = tool.description or "",
        #             input_schema = tool.input_schema
        #         ) for tool in result.tools
        #     ]

        #     return tools
        result = await self.client.list_tools()
            
        tools = [
            Tool(
                name = tool.name,
                description = tool.description or "",
                input_schema = tool.input_schema
            ) for tool in result.tools
        ]

        return tools

    async def call_tool(
        self,
        #name: str,
        tool_call: ToolCall
    ) -> ToolResult:

        # async with self.client:
        #     result = await self.client.call_tool(
        #         name = tool_call.tool_name,
        #         arguments = tool_call.arguments
        #     )

        #     tool_result = ToolResult(
        #         tool_call_id = tool_call.id, 
        #         name = tool_call.tool_name,
        #         #content = 
        #         structured_content = tool_call.structured_content,
        #         is_error = result.is_error
        #     )

        #     return tool_result
        result = await self.client.call_tool(
            name = tool_call.tool_name,
            arguments = tool_call.arguments
        )

        tool_result = ToolResult(
            tool_call_id = tool_call.id, 
            name = tool_call.tool_name,
            #content = 
            structured_content = result.structured_content,
            is_error = result.is_error
        )

        return tool_result
    
    async def __aenter__(self):
        await self.client.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.client.__aexit__(
            exc_type,
            exc_value,
            traceback,
        )
