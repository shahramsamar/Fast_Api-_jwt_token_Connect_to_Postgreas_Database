from sqlalchemy import Column, String,Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database.database import Base
from datetime import datetime
    

class TokenModel(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True, autoincrement=True)
    token = Column(String, unique=True, index=True, nullable=False)
    expiration_date = Column(DateTime,nullable=False)
    user_id = Column(Integer, ForeignKey("authentication.id"))
    user = relationship("AuthModel", back_populates="tokens")
     