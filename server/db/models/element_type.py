from sqlalchemy import Column, Integer, String, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import ARRAY
from server.db.base import Base

class ElementType(Base):
    __tablename__ = "element_types"

    id = Column(Integer, primary_key=True, index=True)
    zone_length = Column(Integer)
    zone_width = Column(Integer)
    title = Column(String)
    description = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    vertices = Column(ARRAY(Integer))