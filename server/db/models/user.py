from sqlalchemy import Column, Integer, String, select
from sqlalchemy.orm import relationship
from passlib.context import CryptContext
from server.db.base import Base

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    org_id = Column(Integer)
    role = Column(String)

    org = relationship("Org", back_populates = "members")
    projects = relationship("Project", back_populates="user", cascade="all, delete-orphan")

    def verify_password(self, plain_password: str) -> bool:
        return pwd_context.verify(plain_password, self.hashed_password)

    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)
    
    @staticmethod
    async def get_user_by_username(db, username: str):
        result = await db.execute(
        select(User).where(User.username == username)
        )
        return result.scalar_one_or_none()
        
    @staticmethod
    async def get_user_by_email(db, email: str):
        result = await db.execute(
        select(User).where(User.email == email)
        )

        return result.scalar_one_or_none()
