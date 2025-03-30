from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from config.database import Base

    
class Questionare(Base):
    __tablename__ = "questionare"

    id=Column(Integer, primary_key=True, index=True)
    title=Column(String(25))
    
    
    