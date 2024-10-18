from sqlalchemy import Column, String,Integer
from database.database import Base
from sqlalchemy.orm import relationship



class AuthModel(Base):
    __tablename__ = "authentication"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    tokens = relationship("TokenModel", back_populates="user")