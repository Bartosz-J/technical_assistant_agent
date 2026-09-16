from technical_assistant_agent.models.agent_state import AgentState
from technical_assistant_agent.models.agent_stop_reason import AgentStopReason

class AgentPolicy:

    def __init__(
        self,
        max_iterations: int,
        max_tool_calls: int,
        #agent_stop_reason: AgentStopReason
    ) -> None:

        self.max_iterations = max_iterations
        self.max_tool_calls = max_tool_calls

        #self.agent_stop_reason = agent_stop_reason

    def run_check(
        self,
        agent_state: AgentState,
        #agent_stop_reason: AgentStopReason
    ) -> AgentStopReason | None:

        if agent_state.iteration >= self.max_iterations:
            return AgentStopReason.MAX_ITERATIONS
            #agent_state.stop_reason = AgentStopReason.MAX_ITERATIONS
            #return False

        if agent_state.tool_calls >= self.max_tool_calls:
            return AgentStopReason.MAX_TOOL_CALLS
            #agent_state.stop_reason = AgentStopReason.MAX_TOOL_CALLS
            #return False

        return None