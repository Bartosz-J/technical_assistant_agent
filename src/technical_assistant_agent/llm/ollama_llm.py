from technical_assistant_agent.llm.base import LLM
from technical_assistant_agent.models.chat_message import ChatMessage
from technical_assistant_agent.models.chat_history import ChatHistory
from technical_assistant_agent.models.llm_response import LLMResponse
from technical_assistant_agent.models.tool import Tool
from technical_assistant_agent.models.tool_call import ToolCall
from technical_assistant_agent.models.tool_result import ToolResult
from ollama import AsyncClient
from uuid import uuid4

import json
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

        # print("\n\n\nwiadomosc przekazywana do Ollama: ")
        # print(messages)


        response = await self.client.chat(
            model = self.model,
            messages = messages,
            tools = ollama_tools,
            # options = {
            #     "temperature": 0.0,
            #     "num_predict": 2048
            # }
            #options = self._map_options(options)
        )

        # dlaczego gemma tak szybko obcina odpowiedz?

        print("\n========== LLM RESPONSE ==========")
        print("content:")
        print(repr(response.message.content))

        print("tool_calls:")
        print(response.message.tool_calls)

        print("done:", response.done)
        print("done_reason:", response.done_reason)
        print("eval_count:", getattr(response, "eval_count", None))

        print("==================================\n")

        return self._map_response(response)

    def _map_messages(
        self,
        chat_history: ChatHistory
    ) -> list[dict[str, Any]]:

        # print("\n\nchat history w _map_messages: ")
        # print(chat_history)
        # ollama_messages_format = [
        #     {
        #         "role": message.role,
        #         "content": message.content
        #     }
        #     for message in chat_history.messages
        # ]

        ollama_messages: list[dict[str, Any]] = []

        for message in chat_history.messages:
            # w zaleznosci od usera, czy typu wiasdomosci (tool_call czy zwykla wiadomosc) trzeba te odpowiedzi inaczej obsluzyc
            # USER, SYSTEM
            if message.role in ('user', 'system'):
                ollama_messages.append({
                    "role": message.role,
                    "content": message.content or ""
                })
                continue

            # ASSISTANT
            if message.role == 'assistant':
                assistant_message: dict[str, Any] = {
                    "role": "assistant",
                    "content": message.content or ""
                }

                # WYWOLANIA TOOLi
                if message.tool_calls:
                    assistant_message["tool_calls"] = [
                        {
                            "function": {
                                "name": tool_call.tool_name,
                                "arguments": tool_call.arguments
                            }
                        } for tool_call in message.tool_calls
                    ]
                ollama_messages.append(assistant_message)

                # WYNIKI TOOLi
                for tool_call in message.tool_calls:
                    if tool_call.result is None:
                        continue

                    ollama_messages.append({
                        "role": "tool",
                        "content": self._map_tool_result(tool_call.result) #(
                            #tool_call.result.content
                            #or str(tool_call.result.structured_content)
                        
                    })
                continue
            raise ValueError(
                f"Nieobslugiwana rola wiadomosci: {message.role}"
            )

        #print("\n\n ollama messages: ")
        #print(ollama_messages)
        return ollama_messages

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
                id = str(uuid4()),
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

    def _map_tool_result(
        self,
        result: ToolResult
    ) -> str:

        if result.content is not None:
            return result.content

        if result.structured_content is not None:
            return json.dumps(
                result.structured_content,
                ensure_ascii=False,
                default=str,
            )
