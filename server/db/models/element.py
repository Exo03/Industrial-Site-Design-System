from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from db.base import Base

class Element(Base):
    __tablename__ = "elements"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete = "CASCADE"), index=True, nullable=False)
    element_type_id = Column(Integer)
    x = Column(Integer)
    y = Column(Integer)
    rotation = Column(Integer)

    __table_args__ = (
        UniqueConstraint('x', 'y', 'project_id', name = "unique_coordinates_per_project"),
    )

    project = relationship("Project", back_populates="elements")
