from technical_assistant_agent.llm.base import LLM
from technical_assistant_agent.models.chat_message import ChatMessage
from technical_assistant_agent.models.chat_history import ChatHistory
from technical_assistant_agent.models.llm_response import LLMResponse
from technical_assistant_agent.models.tool import Tool
from ollama import AsyncClient

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

        response = await self.client.chat(
            model = self.model,
            messages = messages,
            #tools = ollama_tools,
            #options = self._map_options(options)
        )

        print(response)
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
            for message in chat_history.messsages
        ]
        #print(ollama_messages_format)
        return ollama_messages_format

    def _map_tools(
        self,
        tools: list[Tool]
    ):
        pass

    def _map_response(
        self,
        response: Any
    ) -> LLMResponse:

        # Stad mozna wyciagnac dodatkowe informacje np. czas generowania odpowiedzi
        # i zapisac jak dodatkowy parametr LLMResponse, na przyklad w przyszlosci do prowadzenia statystyk
        # liczba tokenow, czas odpowiedzi itd
        # print(response)

        message = ChatMessage(
            role = response.message.role,
            content = response.message.content
        )

        return LLMResponse(
            message = message
        )