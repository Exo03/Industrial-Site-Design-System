from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint, String
from sqlalchemy.orm import relationship
from server.db.base import Base

class Element(Base):
    __tablename__ = "elements"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete = "CASCADE"), index=True, nullable=False)
    element_type_id = Column(Integer, ForeignKey("element_types.id"), index=True, nullable=False)
    x = Column(Integer)
    y = Column(Integer)
    title = Column(String)
    color = Column(String)

    project = relationship("Project", back_populates="elements")

