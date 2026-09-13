from technical_assistant_agent.tools.registry import ToolRegistry
from technical_assistant_agent.llm.llm import LLM

from technical_assistant_agent.models.agent_result import AgentResult
from technical_assistant_agent.models.agent_state import AgentState

class Agent:
    def __init__(
        self,
        llm: LLM,
        tools: ToolRegistry,
        # policy: AgentPolicy      
    ):
        self.llm = llm
        self.tools = tools

    async def run(
        self,
        prompt: str
    ) -> AgentResult:

        agent_state = AgentState(
            user_message = prompt
        )

        return await self._agent_loop(prompt)

    async def _agent_loop(
        self,
        agent_state: AgentState
    ) -> AgentResult:

        while not agent_state.finished:
            pass
            # sprawdzamy czy warunki spelnione
            # np. nie przekroczono dostepnej liczby iteracji