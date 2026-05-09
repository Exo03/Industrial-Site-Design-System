from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None
    vertices: tuple

class ProjectResponse(BaseModel):
    id: int
    name: str
    description: str
    vertices: tuple

    class Config:
        from_attributes = True

class ProjectResize(BaseModel):
    id: int
    vertices: tuple

class ProjectRename(BaseModel):
    id: int
    name: str
    description: str