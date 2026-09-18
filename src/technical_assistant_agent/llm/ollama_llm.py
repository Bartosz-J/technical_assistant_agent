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
        model: str,
        temperature: float,
        max_context_length: int,
        max_num_predict: int
    ) -> None:
        
        self.client = AsyncClient(host = host)
        self.model = model
        self.temperature = temperature
        self.max_context_length = max_context_length
        self.max_num_predict = max_num_predict

    async def chat(
        self,
        chat_history: ChatHistory,
        tools: list[Tool] # tutaj a nie w konstruktorze, bo tools nie sa czescia LLM!
    ) -> LLMResponse:
        
        messages = self._map_messages(chat_history)
        ollama_tools = self._map_tools(tools)

        # print("\n========== OLLAMA INPUT ==========")

        # for i, message in enumerate(messages):
        #     print(f"\n--- MESSAGE {i} ---")
        #     print("role:", message.get("role"))
        #     print("content length:", len(message.get("content", "")))
        #     print("content:")
        #     #print(message.get("content", ""))

        # print("\n==================================\n")

        #print("\n\n\nwiadomosc przekazywana do Ollama: ")
        #print(messages)

        response = await self.client.chat(
            model = self.model,
            messages = messages,
            tools = ollama_tools,
            #think = False,
            options = {
                "temperature": self.temperature,
                "num_predict": self.max_num_predict,    
                "num_ctx": self.max_context_length
            }
            #options = self._map_options(options) - ale to juz chyba bedzie przesada...
        )

        # dlaczego gemma tak szybko obcina odpowiedz?

        # print("\n========== LLM RESPONSE ==========")

        # print("content:")
        # print(repr(response.message.content))

        # print("thinking:")
        # print(repr(response.message.thinking))

        # thinking = response.message.thinking or ""

        # print("thinking length:", len(thinking))
        # print("content length:", len(response.message.content or ""))

        # print("tool_calls:")
        # print(response.message.tool_calls)

        # print("done:")
        # print(response.done)

        # print("done_reason:")
        # print(response.done_reason)

        # print("prompt_eval_count:")
        # print(getattr(response, "prompt_eval_count", None))

        # print("eval_count:")
        # print(getattr(response, "eval_count", None))

        # print("==================================\n")

        return self._map_response(response)

    def _map_messages(
        self,
        chat_history: ChatHistory
    ) -> list[dict[str, Any]]:

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
                        "content": self._map_tool_result(tool_call.result)                         
                    })
                continue
            raise ValueError(
                f"Nieobslugiwana rola wiadomosci: {message.role}"
            )

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

        #print("\n\n\n\n Wynik:")
        #print(result)

        if result.content is not None:
            # content jest wynikiem sformatowanym na potrzeby LLMa
            return result.content

        if result.structured_content is not None:
            return json.dumps(
                result.structured_content,
                ensure_ascii=False,
                default=str,
            )

        return ""