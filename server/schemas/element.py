from pydantic import BaseModel

class ElementCreate(BaseModel):
    project_id: int
    element_type_id: int
    x: int
    y: int
    width: int
    length: int
    title: str
    color: str

class ElementResponse(BaseModel):
    id: int
    element_type_id: int
    x: int
    y: int
    width: int
    length: int
    title: str
    color: str

    class Config:
        from_attributes = True

class ElementMove(BaseModel):
    id: int
    x: int
    y: int

class ElementResize(BaseModel):
    id: int
    width: int
    length: int