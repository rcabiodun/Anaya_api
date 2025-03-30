
from . import schemas
from config.database import get_db
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from .models import User
from sqlalchemy.exc import OperationalError, SQLAlchemyError
from config.exceptions import DatabaseError, DatabaseConnectionError
from sqlalchemy import or_
from .utils import hash_password, verify_password, generate_otp
from utils.jwt import create_access_token
from datetime import datetime, timedelta
from utils.emailUtil import send_verification_email


class AuthenticationController:
  def __init__(self, db: Session):
    self.db = db
    self.User_query=self.db.query(User)

  async def registration(self, request: schemas.CreateUser):
    
    user = request.model_dump()
    print(f"Receiving {user}")
    result=self.User_query.filter(or_(User.email == user["email"],User.phone_number == user["phone_number"])).first()
    if result:
      raise HTTPException(status_code=400, detail="Email/phone-number already registered")
    
    user["password"]=hash_password(user["password"])
    user["otp"]=generate_otp()
    db_item = User(**user)
    self.db.add(db_item)
    self.db.commit()
    self.db.refresh(db_item)
    send_verification_email(user["email"], user["otp"])
    return db_item

  async def login(self, email: str, password: str) -> dict:
    """Authenticate user and return token."""
    user = self.User_query.filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    if not verify_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Create access token with proper claims
    access_token = create_access_token(
        data={
            "sub": user.email,  # subject claim
            "type": user.type,  # custom claim
            "iat": datetime.utcnow(),  # issued at claim
        }
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }


  # async def login_controller(request: LoginRequest) -> LoginResponse:
  #   # This is a placeholder implementation
    
  #   # return LoginResponse(
  #   #     message=f"Login attempt received for user: {request.username}",
  #   #     status=True
  #   # )


  async def users_list_controller(self) :
    # This is a placeholder implementation
    return  self.db.query(User).all()

  async def generate_and_save_otp(self, user_email: str) -> str:
    """Generate OTP and save it to user record."""
    user = self.User_query.filter(User.email == user_email).first()
    if not user:
      raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found"
      )
    
    otp = generate_otp()
    user.otp = otp
    self.db.commit()
    return otp

  async def verify_otp(self, user_email: str, otp: str) -> bool:
    """Verify OTP for user. and return access_token if verified"""
    user = self.User_query.filter(User.email == user_email).first()
    if not user:
      raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found"
      )
    
    if user.otp != otp:
      return (False, "")
    
    # If OTP matches, mark email as verified
    access_token = create_access_token(
        data={
            "sub": user.email,  # subject claim
            "type": user.type,  # custom claim
            "iat": datetime.utcnow(),  # issued at claim
        }
    )
    user.is_email_verified = True
    user.otp = None  # Clear OTP after successful verification
    self.db.commit()
    
    return (True, access_token)


