from functools import lru_cache
from fastapi import Request
from technical_assistant_agent.agent.agent import Agent
# from technical_assistant_agent.config import settings
# from technical_assistant_agent.tools.mcp_tool_provider import MCPToolProvider
# from technical_assistant_agent.llm.base import LLM
# from technical_assistant_agent.llm.ollama_llm import OllamaLLM

# @lru_cache
# def get_mcp_tool_provider() -> MCPToolProvider:
#     return MCPToolProvider(mcp_server_url = settings.mcp_server_url)


# @lru_cache
# def get_ollama_llm() -> OllamaLLM:
#     llm: LLM = OllamaLLM(
#         host = settings.ollama_host,
#         model = settings.ollama_model,
#         temperature = settings.ollama_model_temperature,
#         max_context_length = settings.ollama_max_context_length,
#         max_num_predict = settings.ollama_max_num_predict
#     )

#     return llm

def get_agent(request: Request) -> Agent:
    return request.app.state.agent 