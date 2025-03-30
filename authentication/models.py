from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func, Boolean
from config.database import Base

# all models build must be imported in the migrations/env.py file to work

    
class User(Base):
    __tablename__ = "users"

    id=Column(Integer, primary_key=True, index=True)
    fullname=Column(String)
    email=Column(String, unique=True, index=True)
    type=Column(String)
    phone_number=Column(String)
    otp=Column(String(4))
    is_email_verified=Column(Boolean, default=False,index=True)
    password=Column(String)
    date_created=Column(DateTime, default=func.now())
    
    
    
    