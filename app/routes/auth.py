from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import hash_password

router = APIRouter()

# DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    
    # 1. Check if user already exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # 2. Hash password
    hashed_password = hash_password(user.password)

    # 3. Create user object
    new_user = User(
        email=user.email,
        password=hashed_password,
        role=user.role
    )

    # 4. Save to DB
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # 5. Return response
    return {
        "message": "User created successfully",
        "user_id": new_user.id
    }