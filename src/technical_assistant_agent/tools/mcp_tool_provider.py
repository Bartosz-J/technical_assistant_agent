from mcp import Client
from technical_assistant_agent.tools.tool_provider import ToolProvider
from technical_assistant_agent.models.agent_context import AgentContext
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
        tool_call: ToolCall,
        agent_context: AgentContext
    ) -> ToolResult:

        machine_id = agent_context.machine_id
        user_id = agent_context.user_id

        if machine_id is None:
            raise ValueError("AgentContext nie zawiera machine_id!")

        if user_id is None:
            raise ValueError("AgentContext nie zawiera user_id!")

        result = await self.client.call_tool(
            name = tool_call.tool_name,
            arguments = tool_call.arguments,
            meta = {                            # dodatkowy argument ktory sluzy do przekazywania dodatkowych informacji razem z wywolaniem toola
                "machine_id": int(machine_id)
            }
        )

        tool_result = ToolResult(
            tool_call_id = tool_call.id, 
            name = tool_call.tool_name,
            content = self._build_llm_content(
                tool_name = tool_call.tool_name,
                structured_content = result.structured_content
            ),
            structured_content = result.structured_content,
            is_error = result.is_error
        )

        return tool_result

    def _build_llm_content(
        self,
        tool_name: str,
        structured_content: Any
    ) -> str:

        if tool_name == 'search_documentation':

            search_doc_context = self._format_search_documentation(
                structured_content = structured_content
            )
            return search_doc_context

        # jezeli nie chcemy jakos obrabiac outputu - zwracamy surowy wynik
        return str(structured_content)

        # ewentualnie mozemy wymagac dodania wyniku rowniez tutaj:
        # raise ValueError(
        #     f"Wyniki {tool_name} nie zostal odpowiednio sformatowany dla agenta!"
        # )

    def _format_search_documentation(
        self,
        structured_content: Any
    ) -> str:

        results = structured_content.get("results", [])

        if not results:
            return str(structured_content)

        formatted_results: list[str] = []

        for index, result in enumerate(results, start = 1):
            text = result.get("text","")
            document_title = result.get("document_title", "")
            document_page = result.get("page", "")
            score = result.get("score", "")

            formatted_results.append(
                f"""[Wynik {index}]
Dokument: {document_title}
Strona: {document_page}
Score: {score}

{text}"""
            )

        return "\n\n".join(formatted_results)
    
    async def __aenter__(self):
        await self.client.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.client.__aexit__(
            exc_type,
            exc_value,
            traceback,
        )
