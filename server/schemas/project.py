from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None
    width: int
    length: int

class ProjectResponse(BaseModel):
    id: int
    name: str
    description: str
    width: int
    length: int

    class Config:
        from_attributes = True

class ProjectResize(BaseModel):
    id: int
    width: int
    length: int

class ProjectRename(BaseModel):
    id: int
    name: str
    description: str