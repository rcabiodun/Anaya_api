import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi import HTTPException, status
from dotenv import load_dotenv

load_dotenv()

# Email configuration
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USERNAME = os.getenv("EMAIL_USERNAME")
EMAIL_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")  # This should be an App Password from Google
EMAIL_FROM = os.getenv("EMAIL_FROM", EMAIL_USERNAME)

if not all([EMAIL_USERNAME, EMAIL_PASSWORD]):
    raise ValueError("Email credentials must be set in .env file")

def create_email_template(otp: str, issue: str = "email") -> str:
    """Create HTML email template."""
    return f"""
    <html>
        <body style="font-family: Arial, sans-serif; padding: 20px;">
            <h2>Verify Your Email</h2>
            <p>Your verification code is:</p>
            <h1 style="color: #4CAF50; font-size: 32px;">{otp}</h1>
            <p>This code will expire in a couple of minutes.</p>
            <p>If you didn't request this code, please ignore this email.</p>
        </body>
    </html>
    """

def send_verification_email(to_email: str, otp: str, issue: str = "email") -> bool:
    """
    Send verification email with OTP.
    
    Args:
        to_email: Recipient email address
        otp: One-time password
        issue: Type of verification (default: "email")
    
    Returns:
        bool: True if email sent successfully
    
    Raises:
        HTTPException: If email sending fails
    """
    try:
        # Create message
        if issue=="email":
            message = MIMEMultipart("alternative")
            message["Subject"] = "Email Verification Code"
            message["From"] = EMAIL_FROM
            message["To"] = to_email

            # Create HTML content
            html_content = create_email_template(otp, issue)
            html_part = MIMEText(html_content, "html")
            message.attach(html_part)

            # Create SMTP session
            with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
                server.starttls()
                server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
                server.send_message(message)

            return True

    except Exception as e:
        print(f"Error sending email: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send verification email"
        )

