#from technical_assistant_agent.
from fastapi import APIRouter, Depends
from technical_assistant_agent.app.dependencies import get_agent
from technical_assistant_agent.models.chat_call import ChatCall
from technical_assistant_agent.models.agent_context import AgentContext
from technical_assistant_agent.agent.agent import Agent
from technical_assistant_agent.prompts.system import SYSTEM_PROMPT
from technical_assistant_agent.models.agent_state import AgentState
from technical_assistant_agent.models.chat_message import ChatMessage
from technical_assistant_agent.models.chat_history import ChatHistory
from technical_assistant_agent.models.agent_response import AgentResponse

router = APIRouter(
    prefix = '/agent',
    tags = ['Technical assistant']
)

@router.post('/chat',
             response_model = AgentResponse)#AgentState)
async def chat(
    chat_call: ChatCall,
    agent: Agent = Depends(get_agent)
) -> AgentResponse: #AgentState:

    chat_history = buiild_agent_chat_history(
        chat_call = chat_call
    )

    agent_state = AgentState(
        user_message=chat_call.message,
        chat_history=chat_history #chat_call.chat_history,
    )
    # koniec problematycznego fragmentu

    agent_context = AgentContext(
        user_id=chat_call.agent_context.user_id,
        machine_id=chat_call.agent_context.machine_id,
    )

    return await agent.run(
        agent_state=agent_state,
        agent_context=agent_context,
    )

def buiild_agent_chat_history(
    chat_call: ChatCall
) -> ChatHistory:
    
    system_prompt = ChatMessage(
        role = 'system',
        content = SYSTEM_PROMPT
    )

    chat_history = ChatHistory(
        messages = [system_prompt]
    )
    chat_history.messages = chat_history.messages + chat_call.chat_history.messages

    return chat_history
    