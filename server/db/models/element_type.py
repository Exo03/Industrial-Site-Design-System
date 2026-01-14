from sqlalchemy import Column, Integer, String
from server.db.base import Base

class ElementType(Base):
    __tablename__ = "element_types"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)