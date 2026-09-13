from pydantic import BaseModel
from technical_assistant_agent.models.bounding_box import BoundingBox

# kopia klasy z backendu
class Context(BaseModel):
    chunk_id: str
    text: str
    score: float

    document_id: str
    document_title: str

    page: int

    page_width: float | None = None
    page_height: float | None = None

    bbox: BoundingBox | None = None

    document_url: str | None = None
    page_image_url: str | None = None
    thumbnail_url: str | None = None