from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None

class ProjectResponse(BaseModel):
    id: int
    name: str
    description: str

    class Config:
        from_attributes = True