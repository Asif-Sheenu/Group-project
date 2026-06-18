from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
import os

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_USERNAME"),
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True
)

async def send_otp_email(email: str, otp: str):

    message = MessageSchema(
        subject="Your OTP Code",
        recipients=[email],
        body=f"""
Your OTP is: {otp}

This OTP expires in 5 minutes.
""",
        subtype="plain"
    )

    fm = FastMail(conf)

    await fm.send_message(message)

async def send_otp_email(email: str, otp: str):

    print("Sending OTP to:", email)
    print("OTP:", otp)

    message = MessageSchema(
        subject="Your OTP Code",
        recipients=[email],
        body=f"Your OTP is {otp}",
        subtype="plain"
    )

    fm = FastMail(conf)

    await fm.send_message(message)

    print("Email send completed")