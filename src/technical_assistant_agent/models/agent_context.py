from pydantic import BaseModel
from uuid import UUID

# sluzy do zawezenia kontekstu pracy agenta
# np do danej maszyny lub w przyszlosci - do uprawanien danego uzytkownika
class AgentContext(BaseModel):
    machine_id: str | None = None
    conversation_id: UUID | None = None
    user_id: str | None = None