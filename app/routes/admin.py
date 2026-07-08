from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.admin import get_all_users, get_all_dogs,get_all_cats

router = APIRouter()


@router.get("/users")
def fetch_all_users(db: Session = Depends(get_db)):
    return get_all_users(db)


@router.get("/dogs")
def fetch_all_pets(db: Session = Depends(get_db)):
    return get_all_dogs(db)

@router.get("/cats")
def fetch_all_pets(db: Session = Depends(get_db)):
    return get_all_cats(db)