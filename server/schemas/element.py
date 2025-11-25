from pydantic import BaseModel

class ElementCreate(BaseModel):
    project_id: int
    element_type_id: int
    x: int
    y: int

class ElementResponse(BaseModel):
    id: int
    element_type_id: int
    x: int
    y: int
    rotation: int

    class Config:
        from_attributes = True

class ElementUpdate(BaseModel):
    id: int
    x: int
    y: int
    rotation: int