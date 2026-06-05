from fastapi import APIRouter, HTTPException
from app.core.database import supabase
from app.schemas.user import UserCreate
from app.core.security import hash_password

from app.utils.otp import generate_otp
from app.services.redis_service import redis_client
from app.services.email_service import send_otp_email

from app.schemas.user import VerifyOTP
from app.core.jwt_handler import create_access_token

from app.schemas.user import ResendOTP

from app.schemas.user import LoginSchema
from app.core.security import verify_password
from app.core.jwt_handler import create_access_token

import json

router = APIRouter()


@router.post("/signup")
async def signup(user: UserCreate):

    # 1. Check password match
    if user.password != user.confirm_password:
        raise HTTPException(
            status_code=400,
            detail="Passwords do not match"
        )

    # 2. Password length check
    if len(user.password) > 72:
        raise HTTPException(
            status_code=400,
            detail="Password must be less than 72 characters"
        )

    # 3. Check existing user
    existing_user = supabase.table("users") \
        .select("*") \
        .eq("email", user.email) \
        .execute()

    if existing_user.data:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    # 4. Generate OTP
    otp = generate_otp()

    # 5. Hash password
    hashed_password = hash_password(user.password)

    # 6. Temporary store data
    temp_data = {
        "name": user.name,
        "email": user.email,
        "password": hashed_password,
        "role": user.role,
        "otp": otp
    }

    # 7. Store in Redis for 5 mins
    redis_client.setex(
        f"otp:{user.email}",
        300,
        json.dumps(temp_data)
    )

    # 8. Send OTP Email
    await send_otp_email(user.email, otp)

    # 9. Return response
    return {
        "message": "OTP sent to your email"
    }

@router.post("/verify-otp")
def verify_otp(data: VerifyOTP):

    stored_data = redis_client.get(f"otp:{data.email}")

    if not stored_data:
        raise HTTPException(
            status_code=400,
            detail="OTP expired or not found"
        )

    user_data = json.loads(stored_data)

    if user_data["otp"] != data.otp:
        raise HTTPException(
            status_code=400,
            detail="Invalid OTP"
        )

    # insert into supabase
    response = supabase.table("users").insert({
        "name": user_data["name"],
        "email": user_data["email"],
        "password": user_data["password"],
        "role": user_data["role"]
    }).execute()

    # delete otp from redis
    redis_client.delete(f"otp:{data.email}")

    # generate jwt token
    token = create_access_token({
        "email": user_data["email"]
    })

    return {
        "message": "Registration successful",
        "access_token": token,
        "user": response.data
    }

@router.post("/resend-otp")
async def resend_otp(data: ResendOTP):

    stored_data = redis_client.get(f"otp:{data.email}")

    if not stored_data:
        raise HTTPException(
            status_code=400,
            detail="OTP expired or signup not found"
        )

    user_data = json.loads(stored_data)

    # generate new otp
    new_otp = generate_otp()

    user_data["otp"] = new_otp

    # store again with fresh expiry
    redis_client.setex(
        f"otp:{data.email}",
        300,
        json.dumps(user_data)
    )

    # send email
    await send_otp_email(data.email, new_otp)

    return {
        "message": "New OTP sent successfully"
    }

@router.post("/login")
def login(user: LoginSchema):

    existing_user = supabase.table("users") \
        .select("*") \
        .eq("email", user.email) \
        .execute()

    if not existing_user.data:
        raise HTTPException(
            status_code=400,
            detail="Invalid email or password"
        )

    db_user = existing_user.data[0]

    if not verify_password(
        user.password,
        db_user["password"]
    ):
        raise HTTPException(
            status_code=400,
            detail="Invalid email or password"
        )

    token = create_access_token({
        "email": db_user["email"],
        "role": db_user["role"]
    })

    return {
        "message": "Login successful",
        "access_token": token,
        "user": {
            "id": db_user.get("id"),
            "name": db_user["name"],
            "email": db_user["email"],
            "role": db_user["role"]
        }
    }