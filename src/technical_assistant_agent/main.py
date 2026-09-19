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
        model = settings.ollama_model,
        temperature = settings.ollama_model_temperature,
        max_context_length = settings.ollama_max_context_length,
        max_num_predict = settings.ollama_max_num_predict
    )


    async with MCPToolProvider(
        mcp_server_url = settings.mcp_server_url
    ) as mcp_provider:

        tools = await mcp_provider.list_tools()

        tool_registry = ToolRegistry(tools = tools)


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
            user_message = "Przeszukaj dokumentacje techniczna. skorzystaj z dostepnych narzedzi. Podaj instrukcje obcinania kotew. Nastepnie opis multiplikatora.",
            chat_history = chat_history
        )

        agent_state = await agent.run(
            agent_state = agent_state,
            agent_context = agent_context
            #prompt = "Jak obcinac kotwy?",
            #context = agent_context
        )

        print("\n\n ODPOWIEDZ AGENTA:")
        print(agent_state.final_answer)

        # print("\n\n\n final_answer")
        # print(agent_state.final_answer)
        

        # print("\n\n Historia: ")
        # print(chat_history)



if __name__ == '__main__':
    asyncio.run(main())

