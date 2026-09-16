from pydantic import BaseModel
from uuid import UUID
#from technical_assistant_agent.models.chat_history import ChatHistory

# sluzy do zawezenia kontekstu pracy agenta
# np do danej maszyny lub w przyszlosci - do uprawanien danego uzytkownika
# nie przechowujemy historii konwersacji! jest ona zwracana za kazdym razem ze streamlit
class AgentContext(BaseModel):
    user_id: str | None = None
    machine_id: str | None = None
    # chat_history: ChatHistory
    # conversation_id: UUID | None = None
