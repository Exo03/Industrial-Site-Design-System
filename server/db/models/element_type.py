from sqlalchemy import Column, Integer, String
from server.db.base import Base

class ElementType(Base):
    __tablename__ = "element_types"

    id = Column(Integer, primary_key=True, index=True)
    length = Column(Integer)
    width = Column(Integer)
    title = Column(String)
    description = Column(String)