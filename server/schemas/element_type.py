from pydantic import BaseModel

class ElementTypeResponse(BaseModel):
    id: int
    title: str
    length: int
    width: int
    zone_length: int
    zone_width: int
    description: str

class ElementTypeCreate(BaseModel):
    title: str
    length: int
    width: int
    zone_length: int
    zone_width: int
    description: str