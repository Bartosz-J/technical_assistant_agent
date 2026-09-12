from pydantic import BaseModel
from typing import Literal

# kopia klasy z backendu
class BoundingBox(BaseModel):
    left: float
    top: float
    right: float
    bottom: float

    coord_origin: Literal['top-left', 'bottom-left'] = 'bottom-left'