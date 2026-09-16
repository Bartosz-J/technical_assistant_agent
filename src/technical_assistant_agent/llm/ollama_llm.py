from technical_assistant_agent.llm.base import LLM
from technical_assistant_agent.models.chat_message import ChatMessage
from technical_assistant_agent.models.chat_history import ChatHistory
from technical_assistant_agent.models.llm_response import LLMResponse
from technical_assistant_agent.models.tool import Tool
from technical_assistant_agent.models.tool_call import ToolCall
from ollama import AsyncClient
from uuid import uuid4

from typing import Any

class OllamaLLM(LLM):

    def __init__(
        self,
        host: str,
        #client: AsyncClient,
        model: str
    ) -> None:
        
        self.client = AsyncClient(host = host)
        self.model = model

    async def chat(
        self,
        chat_history: ChatHistory,
        tools: list[Tool] # tutaj a nie w konstruktorze, bo tools nie sa czescia LLM!
    ) -> LLMResponse:
        
        messages = self._map_messages(chat_history)
        ollama_tools = self._map_tools(tools)

        # print("lista narzedzi")
        # print(tools)

        # print("narzedzia przekazywane ollama:")
        # print(ollama_tools)
        # print("\n")

        response = await self.client.chat(
            model = self.model,
            messages = messages,
            tools = ollama_tools,
            #options = self._map_options(options)
        )

        # print("\n\nsurowa odpowiedz Ollama:")
        # print(response)
        # print("role:", response.message.role)
        # print("content:", response.message.content)
        # print("tool_calls:", response.message.tool_calls)
        # print("done:", response.done)
        # print("done_reason:", response.done_reason)
        # print("----------------------------")

        return self._map_response(response)

    def _map_messages(
        self,
        chat_history: ChatHistory
    ) -> list[dict[str, Any]]:

        ollama_messages_format = [
            {
                "role": message.role,
                "content": message.content
            }
            for message in chat_history.messages
        ]
        #print(ollama_messages_format)
        return ollama_messages_format

    def _map_tools(
        self,
        tools: list[Tool]
    ) -> list[dict[str, Any]]:
        # tlumaczy moja wewnetrzna definicje tooli na format oczekiwany przez Ollama

        ollama_tools = [
            {
                "type": "function",
                "function":{
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.input_schema
                }
            }
            for tool in tools
        ]

        return ollama_tools

    def _map_response(
        self,
        response: Any
    ) -> LLMResponse:

        tool_calls = []

        for ollama_tool_call in response.message.tool_calls or []:

            tool_call = ToolCall(
                id = str(uuid4),
                tool_name = ollama_tool_call.function.name,
                arguments = ollama_tool_call.function.arguments
            )

            tool_calls.append(tool_call)

        # Stad mozna wyciagnac dodatkowe informacje np. czas generowania odpowiedzi
        # i zapisac jak dodatkowy parametr LLMResponse, na przyklad w przyszlosci do prowadzenia statystyk
        # liczba tokenow, czas odpowiedzi itd
        # print(response)

        message = ChatMessage(
            role = response.message.role,
            content = response.message.content,
            tool_calls = tool_calls
        )

        return LLMResponse(
            message = message
        )