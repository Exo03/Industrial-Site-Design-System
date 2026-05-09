from pydantic import BaseModel
from typing import Optional

class ElementTypeResponse(BaseModel):
    id: int
    title: str
    zone_length: int
    zone_width: int
    description: Optional[str]
    owner_id: int
    vertices: tuple

class ElementTypeCreate(BaseModel):
    title: str
    zone_length: int
    zone_width: int
    description: Optional[str]
    owner_id: int
    vertices: tuple