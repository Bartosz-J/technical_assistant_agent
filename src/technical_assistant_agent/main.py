import asyncio
from mcp import Client
from technical_assistant_agent.agent.agent import Agent
from technical_assistant_agent.agent.agent_policy import AgentPolicy
from technical_assistant_agent.models.agent_context import AgentContext
from technical_assistant_agent.llm.base import LLM
from technical_assistant_agent.llm.ollama_llm import OllamaLLM
from technical_assistant_agent.tools.registry import ToolRegistry
from technical_assistant_agent.models.chat_history import ChatHistory
from technical_assistant_agent.models.chat_message import ChatMessage
from technical_assistant_agent.config import settings
from technical_assistant_agent.tools.mcp_tool_provider import MCPToolProvider
from technical_assistant_agent.tools.tool_executor import ToolExecutor
from technical_assistant_agent.models.tool_call import ToolCall
from technical_assistant_agent.models.agent_stop_reason import AgentStopReason
from technical_assistant_agent.models.agent_state import AgentState
#from technical_assistant_agent.tools.registry import ToolRegistry

async def main():

    llm: LLM = OllamaLLM(
        host = settings.ollama_host,
        model = settings.ollama_model
    )
    # tool_registry = ToolRegistry()

    # agent = Agent(
    #     llm = llm,
    #     tools = tool_registry
    # )

    #print(tool_registry.list_tools)

    # chat_message = ChatMessage(
    #     role = "user",
    #     content = "Przedstaw sie!"
    # )

    # chat_history = ChatHistory()
    # chat_history.add(chat_message)
    # print(chat_history)

    # response = await llm.chat(
    #     chat_history = chat_history,
    #     tools = [])

    # sprawdzamy dostepne narzedzia:
    # async with Client(settings.mcp_server_url) as client:
    #     tools = await client.list_tools()
    #     print("Dostepne narzedzia:")
    #     for tool in tools:
    #         print(tool)

    async with MCPToolProvider(
        mcp_server_url = settings.mcp_server_url
    ) as mcp_provider:

        tools = await mcp_provider.list_tools()

        tool_registry = ToolRegistry(tools = tools)

        #print(tool_registry.list_tools())

        # testujemy odpalanie tooli recznie
        tool_executor = ToolExecutor(
            tool_provider = mcp_provider
        )

        agent_policy = AgentPolicy(
            max_iterations = settings.max_agent_iterations,
            max_tool_calls = settings.max_tool_calls
        )

        agent = Agent(
            llm = llm,
            tools = tool_registry,
            tool_executor = tool_executor,
            agent_policy = agent_policy
        )

        agent_context = AgentContext(
            user_id = '1',
            machine_id = '1'
        )

        chat_history = ChatHistory(
            messages = []
        )

        agent_state = AgentState(
            user_message = "Przeszukaj dokumentacje techniczna. skorzystaj z dostepnych narzedzi. query: jak obcinac kotwy",
            chat_history = chat_history
        )

        agent_response = await agent.run(
            agent_state = agent_state,
            agent_context = agent_context
            #prompt = "Jak obcinac kotwy?",
            #context = agent_context
        )

        #print(agent_response)

        # tool_call = ToolCall(
        #     id = '1',
        #     tool_name = 'search_documentation',
        #     arguments = {
        #         'query': 'jak obcinac_kotwy',
        #         'machine_id': 123,
        #         'limit': 5
        #     },
        # )

        # tool_result = await tool_executor.execute(tool_call = tool_call)
        # print(tool_result)


if __name__ == '__main__':
    asyncio.run(main())

