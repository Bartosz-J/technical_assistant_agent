import asyncio
from mcp import Client
from technical_assistant_agent.agent.agent import Agent
from technical_assistant_agent.llm.base import LLM
from technical_assistant_agent.llm.ollama_llm import OllamaLLM
from technical_assistant_agent.tools.registry import ToolRegistry
from technical_assistant_agent.models.chat_history import ChatHistory
from technical_assistant_agent.models.chat_message import ChatMessage
from technical_assistant_agent.config import settings

async def main():

    print(settings.ollama_host)
    print(settings.ollama_model)

    llm: LLM = OllamaLLM(
        host = settings.ollama_host,
        model = settings.ollama_model
    )
    tool_registry = ToolRegistry()

    agent = Agent(
        llm = llm,
        tools = tool_registry
    )

    #print(tool_registry.list_tools)

    chat_message = ChatMessage(
        role = "user",
        content = "Przedstaw sie!"
    )

    chat_history = ChatHistory()
    chat_history.add(chat_message)
    print(chat_history)

    response = await llm.chat(
        chat_history = chat_history,
        tools = [])

    # sprawdzamy dostepne narzedzia:
    async with Client(settings.mcp_server_url) as client:
        tools = await client.list_tools()
        print("Dostepne narzedzia:")
        for tool in tools:
            print(tool)


if __name__ == '__main__':
    asyncio.run(main())

