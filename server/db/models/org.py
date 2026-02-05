from sqlalchemy import Column, Integer, String, select
from sqlalchemy.orm import relationship
from passlib.context import CryptContext
from server.db.base import Base

class Org(Base):
    __tablename__ = "organisations"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique = True)
    title = Column(String, unique = True)

    members = relationship("User", back_populates = "org")