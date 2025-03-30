from pydantic import BaseModel, EmailStr, constr
from datetime import datetime
from typing import Literal, Optional, Union

class LoginRequest(BaseModel):
    username:Optional[EmailStr]
    # email: Optional[EmailStr]=""
    password: constr(min_length=8)

class LoginResponse(BaseModel):
    token_type: str
    access_token: str 
    message: str
    is_email_verified:bool=False
    email:EmailStr
    status: bool

class CreateUser(BaseModel):
    fullname: str
    password: constr(min_length=8)
    email: EmailStr
    phone_number: str
    type: Literal["regular", "dermatologist"] = "regular"

class User(BaseModel):
    id: int
    fullname: str
    email: EmailStr
    phone_number: str
    type: str
    otp: Union[str, None]
    is_email_verified: bool
    date_created: datetime

    class Config:
        from_attributes = True
