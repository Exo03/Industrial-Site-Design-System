from pydantic import BaseModel

class ElementCreate(BaseModel):
    project_id: int
    element_type_id: int
    x: int
    y: int
    title: str
    color: str

class ElementResponse(BaseModel):
    id: int
    element_type_id: int
    x: int
    y: int
    title: str
    color: str

    class Config:
        from_attributes = True

class ElementMove(BaseModel):
    id: int
    x: int
    y: int


class ElementRename(BaseModel):
    id: int
    title: str

class ElementRecolor(BaseModel):
    id: int
    color: str

