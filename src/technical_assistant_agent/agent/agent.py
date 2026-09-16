from technical_assistant_agent.llm.base import LLM
from technical_assistant_agent.tools.registry import ToolRegistry
from technical_assistant_agent.tools.tool_executor import ToolExecutor

from technical_assistant_agent.models.agent_response import AgentResponse
from technical_assistant_agent.models.agent_state import AgentState
from technical_assistant_agent.models.agent_context import AgentContext
from technical_assistant_agent.agent.agent_policy import AgentPolicy
from technical_assistant_agent.models.chat_message import ChatMessage

class Agent:
    def __init__(
        self,
        llm: LLM,
        tools: ToolRegistry,
        tool_executor: ToolExecutor,
        agent_policy: AgentPolicy      
    ) -> None:
        
        self.llm = llm
        self.tools = tools
        self.tools_executor = tool_executor
        self.agent_policy = agent_policy

    async def run(
        self,
        #prompt: str,
        agent_state: AgentState,
        agent_context: AgentContext   # w przyszlosci do przekazania informacji o maszynie
    ) -> AgentResponse:

        # dodajemy ostatnia wiadomosc do historii konwersacji
        agent_state.chat_history.add(
            ChatMessage(
                role = 'user',
                content = agent_state.user_message
            )
        )

        return await self._agent_loop(
            agent_state = agent_state,
            agent_context = agent_context
        )

    async def _agent_loop(
        self,
        agent_state: AgentState,
        agent_context: AgentContext
    ) -> AgentResponse:

        while not agent_state.finished:
            
            # sprawdzamy czy warunki spelnione
            # np. nie przekroczono dostepnej liczby iteracji
            stop_reason = self.agent_policy.run_check(
                agent_state = agent_state
            )

            if stop_reason is not None:
                agent_state.finished = True
                agent_state.stop_reason = stop_reason
                break

            agent_state.iteration += 1

            print("dostepne narzedzia: ")
            print(self.tools.list_tools())
            print("\n\n\n")

            response = await self.llm.chat(
                chat_history = agent_state.chat_history,
                tools = self.tools.list_tools()
            )

            print(response)
            print("\nwywolane toole:")
            print(response.message.tool_calls)

            break

            