
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from .controller import AuthenticationController
from . import schemas
from config.database import get_db
from sqlalchemy.orm import Session
from utils.deps import get_current_user,oauth2_scheme
from .models import User
from utils.jwt import verify_token
from utils.emailUtil import send_verification_email

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])



@auth_router.post("/registration")
async def registration(request: schemas.CreateUser, db: Session = Depends(get_db)):
    await AuthenticationController(db).registration(request)
    return {"message": "Otp sent to your mail to verify your account"}


@auth_router.post("/login", response_model=schemas.LoginResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    
    Authenticate a user and return an access token.

    This endpoint verifies the provided username/email and password. If the authentication is successful, it generates and returns a JWT access token. The body of the request must be in x-www-form-urlencoded format.

    **THE DATA SENT IN THE USERNAME FIELD MUST BE THE EMAIL OF THE USER**
    Args:

    form_data (OAuth2PasswordRequestForm): The form data containing the username/email and password.
    Returns:

    dict: A dictionary containing the access token and its type.
    Raises:

    HTTPException: If the authentication fails due to incorrect username/email or password.
    
    
    """
    result = await AuthenticationController(db).login(form_data.username, form_data.password)
    
    return schemas.LoginResponse(
        access_token=result["access_token"],
        token_type="bearer",
        message="Login successful",
        is_email_verified=result["user"].is_email_verified,
        email=result["user"].email,
        status=True,
    )



# @auth_router.get("/view-all-users", response_model=list[schemas.User],)
# async def users_list(db:Session=Depends(get_db)):
#   """
#   Authenticate a user with their credentials.

#   Parameters:
#       request (LoginRequest):
#           - username: User's unique identifier
#           - password: User's password (minimum length: 8 characters)

#   Returns:
#       LoginResponse:
#           - message: Status message about the login attempt
#           - status: Boolean indicating success (true) or failure (false)
#   """
#   return await AuthenticationController(db).users_list_controller()


@auth_router.get("/me", response_model=schemas.User)
async def read_users_me(
    current_user: User = Depends(get_current_user)
):
    """Get current authenticated user."""
    return current_user

# Protected route example
@auth_router.get("/protected")
async def protected_route(current_user: User = Depends(get_current_user)):
    """Example of a protected route."""
    return {"message": f"Hello {current_user.fullname}, this is a protected route"}

# @auth_router.get("/debug-token")
# async def debug_token(token: str = Depends(oauth2_scheme)):
#     """Debug endpoint to check token contents."""
#     try:
#         payload = verify_token(token)
#         return {"token_contents": payload}
#     except Exception as e:
#         return {"error": str(e)}

@auth_router.post("/generate-otp/{email}")
async def generate_otp(
    email: str,
    db: Session = Depends(get_db)
):
    """Generate OTP for email verification."""
    otp = await AuthenticationController(db).generate_and_save_otp(email)
    # Here you would typically send the OTP via email
    # For development, we'll return it directly
    send_verification_email(email, otp)
    return {"message": "OTP generated successfully and sent via email", "otp": otp}

@auth_router.post("/verify-otp")
async def verify_otp(
    email: str,
    otp: str,
    db: Session = Depends(get_db)
):
    """Verify OTP and mark email as verified."""
    is_valid, access_token = await AuthenticationController(db).verify_otp(email, otp)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid OTP"
        )
    return {"message": "Email verified successfully","access_token":access_token,"token_type":"bearer"}

