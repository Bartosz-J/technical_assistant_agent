from enum import Enum

class AgentStopReason(str, Enum):
    COMPLETED = 'completed'
    MAX_ITERATIONS = 'max_iterations'
    MAX_TOOL_CALLS = 'max_tool_calls'