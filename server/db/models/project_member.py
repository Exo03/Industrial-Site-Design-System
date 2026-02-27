from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from server.db.base import Base

class ProjectMember(Base):
    __tablename__ = "project_members"

    user_id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    project_id = Column(Integer, ForeignKey("project.id"), primary_key=True)

    project = relationship("Project", back_populates="members")
    user = relationship("User", back_populates="project_memberships")