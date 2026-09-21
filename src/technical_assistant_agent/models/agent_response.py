from pydantic import BaseModel
from technical_assistant_agent.models.agent_stop_reason import AgentStopReason
from technical_assistant_agent.models.chat_history import ChatHistory

# generalnie bedzie sie w duzej mierze pokrywac z agent_state, ale nie chcemy zwracac absolutnie wszystkiego uzytkownikowi
# np. nie chcemy zwracac system_promptu w chat_history...'
# wiec chat_history bedzie obciete do public_history
class AgentResponse(BaseModel):

    #user_message: str juz jest w chat_history

    chat_history: ChatHistory

    iteration: int = 0
    tool_calls: int = 0

    finished: bool = False

    final_answer: str | None = None
    stop_reason: AgentStopReason | None = None