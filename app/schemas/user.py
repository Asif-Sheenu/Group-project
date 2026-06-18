from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(min_length=6, max_length=72)
    confirm_password: str
    role: str | None = "user"


class VerifyOTP(BaseModel):
    email: EmailStr
    otp: str

class ResendOTP(BaseModel):
    email: EmailStr

class LoginSchema(BaseModel):
    email: EmailStr
    password: str

class GoogleLoginSchema(BaseModel):
    token: str

class RefreshTokenSchema(BaseModel):
    refresh_token: str