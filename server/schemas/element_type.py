from pydantic import BaseModel

class ElementTypeResponse(BaseModel):
    id: int
    title: str
    description: str