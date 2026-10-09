from fastapi import FastAPI
from contextlib import asynccontextmanager
from technical_assistant_agent.config import settings

#from technical_assistant_agent.app.dependencies import get_ollama_llm, get_mcp_tool_provider

from technical_assistant_agent.llm.base import LLM
from technical_assistant_agent.llm.ollama_llm import OllamaLLM

from technical_assistant_agent.agent.agent_policy import AgentPolicy

from technical_assistant_agent.tools.mcp_tool_provider import MCPToolProvider
from technical_assistant_agent.tools.registry import ToolRegistry
from technical_assistant_agent.tools.tool_executor import ToolExecutor

from technical_assistant_agent.agent.agent import Agent
from technical_assistant_agent.app.routers import agent


@asynccontextmanager
async def lifespan(
    app: FastAPI
):
    llm: LLM = OllamaLLM(
        host = settings.ollama_host,
        model = settings.ollama_model,
        temperature = settings.ollama_model_temperature,
        max_context_length = settings.ollama_max_context_length,
        max_num_predict = settings.ollama_max_num_predict
    )


    mcp_provider = MCPToolProvider(
        mcp_server_url = settings.mcp_server_url
    )

    async with mcp_provider:
        tools = await mcp_provider.list_tools()
        tool_registry = ToolRegistry(tools = tools)

        print("dostepne narzedzia:")
        print(tools)

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

        app.state.agent = agent

        yield
    

api = FastAPI(
    lifespan = lifespan,
    
)

api.include_router(agent.router)