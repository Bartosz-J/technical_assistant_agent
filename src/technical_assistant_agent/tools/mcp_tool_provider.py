from mcp import Client
from technical_assistant_agent.tools.tool_provider import ToolProvider
from technical_assistant_agent.models.agent_context import AgentContext
from technical_assistant_agent.models.tool import Tool
from technical_assistant_agent.models.tool_call import ToolCall
from technical_assistant_agent.models.tool_result import ToolResult

from uuid import UUID
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
        result = await self.client.list_tools()
            
        tools = [
            Tool(
                name = tool.name,
                description = tool.description or "",
                input_schema = tool.input_schema
            ) for tool in result.tools
        ]

        # print("dostepne narzedzia:")
        # print(tools)
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

        # print("Kontekst agenta w call_tool")
        # print(agent_context)
        # print("tool_call:")
        # print(tool_call)

        result = await self.client.call_tool(
            name = tool_call.tool_name,
            arguments = tool_call.arguments,
            meta = {                            # dodatkowy argument ktory sluzy do przekazywania dodatkowych informacji razem z wywolaniem toola
                "machine_id": machine_id
            }
        )

        #print("Wynik narzedzia")
        #print

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
        '''
        Formatuje output narzedzia zwracany przez MCP zeby byl zjadliwy dla modelu.
        Usuwa m.in. informacje istotne z punktu widzenia wyswietlania obrazkow czy czhunkow contextu.
        '''

        if tool_name == 'search_documentation':

            # print("przekazywany structured_content")
            search_doc_context = self._format_search_documentation(
                structured_content = structured_content
            )
            return search_doc_context
        
        if tool_name == 'full_text_search_documentation':

            full_text_search_context = self._format_full_text_search_documentation(
                structured_content = structured_content
            )

            return full_text_search_context
        
        if tool_name =='search_filtered_documentation':
            print("Wywolano search_filtered_documentation")
            print(structured_content)
        
        if tool_name == 'list_documents':

            list_doc_context = self._format_list_documents(
                structured_content = structured_content
            )

            return list_doc_context
        
        if tool_name == 'search_pictures':

            search_pict_content = self._format_search_pictures(
                structured_content = structured_content
            )

            return search_pict_content

        # jezeli nie chcemy jakos obrabiac outputu - zwracamy surowy wynik
        return str(structured_content)

    def _format_search_pictures(
        self,
        structured_content: Any
    ) -> str:

        #print("Wywolano search_pictures!")
        #print(structured_content)

        results = structured_content.get("results", [])

        if not results:
            return str(structured_content)

        formatted_results: list[str] = []

        for index, result in enumerate(results, start = 1):

            # wyciagamy informacje o obrazku
            picture = result.get("picture", {})

            document_id = result.get("document_id", "")
            document_title = result.get("document_title", "")
            
            document_page = picture.get("page", "")
            picture_description = picture.get("description", "")
            picture_caption = picture.get("caption", "")
            #score = result.get("score", "")

            formatted_results.append(
                f"""[Wynik {index}]
                    Dokument: {document_title}
                    Dokument ID: {document_id}
                    Strona obrazka: {document_page}
                    Podpis obrazka: {picture_caption}

                    {picture_description}""".strip()
            )

        return "\n\n".join(formatted_results)

    # wrapper
    def _format_full_text_search_documentation(
        self,
        structured_content: Any
    ) -> str:

        result = self._format_search_documentation(
            structured_content = structured_content
        )

        return result

    def _format_search_filtered_documentation(
        self,
        structured_content: Any
    ) -> str:
        
        result = self._format_search_documentation(
            structured_content = structured_content
        )

        return result

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

                    {text}""".strip()
            )

        return "\n\n".join(formatted_results)

    def _format_list_documents(
        self,
        structured_content: Any
    ) -> str:

        results = structured_content.get("results", [])

        if not results:
            return str(structured_content)

        formatted_results: list[str] = []

        for index, result in enumerate(results, start = 1):

            document_id = result.get("id","")
            document_original_title = result.get("title", "")
            document_generated_title = result.get("generated_title", "")


            formatted_results.append(
                f"""[Wynik {index}]
                    Dokument ID: {document_id}
                    Tytuł: {document_original_title}
                    Tytuł opisowy: {document_generated_title}
                    """.strip()
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
