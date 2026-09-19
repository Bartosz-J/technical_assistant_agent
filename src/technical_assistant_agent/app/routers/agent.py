#from technical_assistant_agent.
from fastapi import APIRouter, Depends
from technical_assistant_agent.app.dependencies import get_agent
from technical_assistant_agent.models.chat_call import ChatCall
from technical_assistant_agent.models.agent_context import AgentContext
from technical_assistant_agent.agent.agent import Agent

from technical_assistant_agent.models.agent_state import AgentState

router = APIRouter(
    prefix = '/agent',
    tags = ['Technical assistant']
)

@router.post('/chat',
             response_model = AgentState)
async def chat(
    chat_call: ChatCall,
    agent: Agent = Depends(get_agent)
) -> AgentState:

    agent_state = AgentState(
        user_message=chat_call.message,
        chat_history=chat_call.chat_history,
    )

    agent_context = AgentContext(
        user_id=chat_call.agent_context.user_id,
        machine_id=chat_call.agent_context.machine_id,
    )

    return await agent.run(
        agent_state=agent_state,
        agent_context=agent_context,
    )