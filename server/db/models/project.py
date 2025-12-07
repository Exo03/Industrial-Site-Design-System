from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from server.db.base import Base

class Project(Base):
        __tablename__ = "projects"

        id = Column(Integer, primary_key=True, index=True)
        name = Column(String)
        description = Column(String)
        owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
        
        elements = relationship("Element", back_populates="project", cascade="all, delete-orphan")

        user = relationship("User", back_populates="projects")
