from sqlalchemy import Column, Integer, String
from .database import Base
# This is the User model for the application
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)
    birth_state = Column(String)
