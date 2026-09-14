from abc import ABC, abstractmethod

from technical_assistant_agent.models.tool import Tool
from technical_assistant_agent.models.chat_history import ChatHistory
from technical_assistant_agent.models.llm_response import LLMResponse


class LLM(ABC):

    @abstractmethod
    async def chat(
        self,
        # message: str,
        chat_history: ChatHistory,
        tools: list[Tool]
    ) -> LLMResponse:
        raise NotImplementedError