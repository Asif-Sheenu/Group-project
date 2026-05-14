from fastapi import APIRouter, HTTPException
from app.core.database import supabase
from app.schemas.user import UserCreate
from app.core.security import hash_password

router = APIRouter()

@router.post("/signup")
def signup(user: UserCreate):

    # 1. Check password match
    if user.password != user.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    
    if len(user.password) > 72:
        raise HTTPException(
            status_code=400,
            detail="Password must be less than 72 characters"
    )

    # 2. Check if user exists
    existing_user = supabase.table("users") \
        .select("*") \
        .eq("email", user.email) \
        .execute()

    if existing_user.data:
        raise HTTPException(status_code=400, detail="Email already registered")

    # 3. Hash password
    hashed_password = hash_password(user.password)

    # 4. Insert into Supabase
    response = supabase.table("users").insert({
        "name": user.name,
        "email": user.email,
        "password": hashed_password,
        "role": user.role
    }).execute()

    # 5. Return response
    return {
        "message": "User created successfully",
        "data": response.data
    }